from django.http import Http404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.response import Response
from ..auction.models import Auction
from django.utils import timezone
from decimal import Decimal
from django.db.models import Max
from .models import Bidding
from .serializers import (
    BiddingListSerializer, CreateBiddingSerializer,
    UpdateDeleteBiddingSerializer, BiddersListSerializer)

"""VIEW/CONTROLLER of the bidding app
    displays, updates, deletes bids placed by authenticated users
    Users can place bids on OPEN auctions/items,"""

'''=============================================='''

"""Create Api View: authenticated users can create items """


class CreateBid(CreateAPIView):
    queryset = Bidding.objects.all()
    serializer_class = CreateBiddingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = request.user
        auction = Auction.objects.get(id=request.data['auction'])
        auction_status = Auction.objects.filter(id=request.data['auction']).values('auction_status')
        highest_bid = Bidding.objects.all().aggregate(Max('bidding_price'))

        if highest_bid['bidding_price__max'] is None:
            highest_bid['bidding_price__max'] = auction.auction_default_price

        if str(auction_status[0]['auction_status']) != str('OPEN'):
            return Response('Auction is Closed or Pending. You can place a bid when the Auction is Open.',
                            status=status.HTTP_400_BAD_REQUEST)
        elif Decimal(highest_bid['bidding_price__max']) > Decimal(request.data['bidding_price']):
            return Response("The highest bid is: " + str(
                highest_bid['bidding_price__max']) + " £. You can only place a bid that is higher.",
                            status=status.HTTP_400_BAD_REQUEST)
        elif user == auction.item.item_owner:
            return Response('You cannot place a bid on your own Item or Auction.', status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid(raise_exception=True):
                if auction.auction_end_time < timezone.now():
                    bid = Bidding.objects.all().first()
                    if bid is not None:
                        bid.auction.auction_winner = bid.bidding_user
                        bid.auction.auction_item_sold = True
                        bid.auction.save()
                        return Response("This Auction is expired. The winner is: " + str(bid.bidding_user),
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(bidding_user=user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""List Api View: authenticated users can view all the previously placed bids on auctions/items
    all information returned: including items, auction, users, bidding details"""


class BiddingList(ListAPIView):
    queryset = Bidding.objects.all()
    serializer_class = BiddingListSerializer


"""List api view: Display all the bidders and their bid associated with a specific auction based on the auction ID <-pk->"""


class AuctionListBidders(ListAPIView):
    queryset = Bidding.objects.all()
    serializer_class = BiddersListSerializer

    def get_queryset(self):
        return Bidding.objects.filter(auction=self.kwargs['pk'])


"""Retrieve Update Destroy APIView: authenticated  user can update, delete his/her own Bid based on the bid ID <-pk->"""


class GetUpdateDeleteBid(RetrieveUpdateDestroyAPIView):
    queryset = Bidding.objects.all()
    serializer_class = UpdateDeleteBiddingSerializer

    """Get a specific Bid based on bidding ID <-> pk"""

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    """Updating a specific Bid. Only the owner of can update his/her previously places bid (price). """

    def update(self, request, *args, **kwargs):
        # global variable to get the owner id of the Auction/Item
        # and the auction instance
        bidding_user = None
        auction = None
        highest_bid = None
        # check if item/auction is exist, otherwise  an error is returned
        try:
            self.object = self.get_object()
            bidding_user = self.get_serializer(self.object)
            auction = Auction.objects.get(id=bidding_user.data['auction']['id'])
            bidding_user = bidding_user.data['bidding_user']['id']
            highest_bid = Bidding.objects.all().aggregate(Max('bidding_price'))
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_400_BAD_REQUEST

            # check if the request user is the owner of the bid, owner of items/auctions cannot bid on their on item or perform update operations
        if int(request.user.id) == int(bidding_user):
            serializer = self.get_serializer(self.object, data=request.data)

            if Decimal(highest_bid['bidding_price__max']) > Decimal(request.data['bidding_price']):
                return Response("The highest bid is: " + str(
                    highest_bid['bidding_price__max']) + " £. You can only update your bid if that is higher.")

            if serializer.is_valid():
                if auction.auction_end_time < timezone.now():
                    bid = Bidding.objects.order_by('bidding_price').first()
                    bid.auction.auction_winner = bid.bidding_user
                    bid.auction.save()
                    return Response("This Auction is expired. The winner is: " + str(bid.bidding_user))
                else:
                    self.object = serializer.save()
                    return Response(serializer.data, status=success_status_code)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # error message to notify user that he/her cannot update other user's bid
            return Response("You can only update your own Bid.")

    """Deleting a Bid: Only the owner of the Bid can perform a delete action, on his/her previously placed bid"""

    def delete(self, request, *args, **kwargs):
        # global variable for later use(assigment) it will contain the owner id of the item/auction
        bidding_user = None
        # checking if item/auction exist
        try:
            self.object = self.get_object()
            bidding_user = self.get_serializer(self.object)
            bidding_user = bidding_user.data['bidding_user']['id']
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_201_CREATED

        # check if request user is the owner of the bid, if not an error message is returned
        if int(request.user.id) == int(bidding_user):
            # deleting the bid from database, returning success message,
            self.object.delete()
            return Response("Bid successfully deleted.", status=success_status_code)
        else:
            # if request user is not the one who placed the bid an error message will returned
            return Response('You can only delete your own Bid.', status=status.HTTP_400_BAD_REQUEST)


# view to return the sum of all the bidders associated with a specific auction
class SumBidders(ListAPIView):
    queryset = Bidding.objects.all()
    serializer_class = BiddingListSerializer

    def get(self, request, **kwargs):
        p = " person"
        message_count = Bidding.objects.filter(auction=self.kwargs['pk']).count()
        if message_count > 1:
            p = " people"
        return Response(
            "Currently " + str(message_count) + p + " is bidding on the item: " + str(Bidding.objects.all().first()),
            status=status.HTTP_200_OK)