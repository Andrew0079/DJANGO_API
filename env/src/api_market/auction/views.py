from .models import Auction
from .serializers import CreateAuctionSerializer, ListAuctionSerializer, WinnerSerializer
from ..items.models import Item
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from django.http import Http404
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

"""Create Api View: authenticated  users can create Auctions """


class CreateAuction(CreateAPIView):
    queryset = Auction.objects.all()
    serializer_class = CreateAuctionSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = request.user
            item = Item.objects.get(id=request.data['item'], item_owner=user)
        except Item.DoesNotExist:
            return Response("You do not own this Item. You can only post items to Auction, that belong to you.",
                            status=status.HTTP_201_CREATED)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            item.__setattr__('item_is_in_auction', True)
            item.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""List Api View: authenticated  users can view Auctions """


class ListAllAuction(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = ListAuctionSerializer


"""Retrieve Update Destroy APIView: authenticated  user can update, delete  his/her own Auction """


class GetUpdateDeleteAuction(RetrieveUpdateDestroyAPIView):
    queryset = Auction.objects.all()
    serializer_class = CreateAuctionSerializer

    """Get specific Auction based on Auction ID <-> pk"""

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    """Updating a specific Auction. Only user who owns the Auction can perform an update action. """

    def update(self, request, *args, **kwargs):
        try:
            # get current auction object
            self.object = self.get_object()
            auction = self.get_serializer(self.object)
            item = Item.objects.get(id=auction.data['item'])
            # Returns the value of the field name for this instance.
            # If the field is a foreign key, returns the id value, instead of the object
            user_id = item.serializable_value('item_owner')
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_201_CREATED

        # check if the request user is the owner of the Auction
        if int(request.user.id) != int(user_id):
            return Response("You do not own this Auction. You can only modify your own Auctions.")

        # saving updated auction's details, and returning the data
        serializer = self.get_serializer(self.object, data=request.data)
        if serializer.is_valid():
            self.object = serializer.save()
            return Response(serializer.data, status=success_status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """Deleting an Auction: Only the owner of the auction can perform a delete action."""

    def delete(self, request, *args, **kwargs):
        try:
            # get current auction object
            self.object = self.get_object()
            auction = self.get_serializer(self.object)
            item = Item.objects.get(id=auction.data['item'])
            # Returns the value of the field name for this instance.
            # If the field is a foreign key, returns the id value, instead of the object
            user_id = item.serializable_value('item_owner')
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_201_CREATED

        # check if request user is the owner of the auction, if not an error message is returned
        if int(request.user.id) != int(user_id):
            return Response("You do not own this auction. You can only delete your own auction.",
                            status=status.HTTP_400_BAD_REQUEST)
        # deleting auction from database, returning success message
        self.object.delete()
        return Response("Auction successfully deleted.", status=success_status_code)


# view to return the COMPLETED, OPEN, or PENDING AUCTIONS
class StatusAuctionList(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = ListAuctionSerializer

    def get_queryset(self):
        if self.kwargs['slug'] == "OPEN":
            return Auction.objects.filter(auction_status='OPEN')
        elif self.kwargs['slug'] == "CLOSED":
            return Auction.objects.filter(auction_status='CLOSED')
        return Auction.objects.filter(auction_status='PENDING')


# return either the expired auctions or the ones that are still available
class NewOrExpiredAuctions(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = ListAuctionSerializer

    def get_queryset(self):
        if self.kwargs['slug'] == 'expired':
            return Auction.objects.filter(Q(auction_end_time__lte=timezone.now()))
        elif self.kwargs['slug'] == 'new':
            return Auction.objects.filter(Q(auction_end_time__gte=timezone.now()))


# return either the expired auctions or the ones that are still available
class WinnersAuction(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = WinnerSerializer

    def get_queryset(self):
        return Auction.objects.filter(~Q(auction_winner=1))


# return all items that are sold in an auction
class SoldAuction(ListAPIView):
    queryset = Auction.objects.all()
    serializer_class = WinnerSerializer

    def get_queryset(self):
        return Auction.objects.filter(auction_item_sold=True)