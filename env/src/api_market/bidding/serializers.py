from rest_framework.serializers import ModelSerializer
from .models import Bidding
from ..auction.serializers import ListAuctionSerializer
from oAuth2Server.serializers import UserSerializer
from rest_framework import serializers


# serializing all bids: returns nested information of users, items, auctions


class BiddingListSerializer(ModelSerializer):
    bidding_user = UserSerializer(read_only=True)
    auction = ListAuctionSerializer(read_only=True)

    class Meta:
        model = Bidding
        fields = ('id', 'auction', 'bidding_user', 'bidding_price')


# serializer to update and delete bids


class UpdateDeleteBiddingSerializer(ModelSerializer):
    bidding_user = UserSerializer(read_only=True)
    auction = ListAuctionSerializer(read_only=True)

    class Meta:
        model = Bidding
        fields = ('id', 'auction', 'bidding_user', 'bidding_price')


# creating a bid: if user is already placed a bid, that specific bid will be updated


class CreateBiddingSerializer(ModelSerializer):
    class Meta:
        model = Bidding
        fields = ('id', 'auction', 'bidding_price', 'bidding_user')
        read_only_fields = ['bidding_user']

    def create(self, validated_data):
        answer, created = Bidding.objects.update_or_create(
            bidding_user=validated_data.get('bidding_user', None),
            auction=validated_data.get('auction', None),
            defaults=validated_data)

        # returns the newly created bid
        return answer

# serializers all the users and their bid associated with a specific auction ID <-pk->


class BiddersListSerializer(ModelSerializer):
    bidding_user = UserSerializer(read_only=True)
    auction = serializers.CharField(source='auction.item.item_title')

    class Meta:
        model = Bidding
        fields = ('id', 'auction', 'bidding_user', 'bidding_price')
