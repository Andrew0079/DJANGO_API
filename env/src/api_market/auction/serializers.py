from rest_framework.serializers import ModelSerializer
from .models import Auction
from ..items.serializers import ListItemSerializer
from oAuth2Server.serializers import UserSerializer

"""serializing all details of the auction, including details of items too"""


class ListAuctionSerializer(ModelSerializer):
    item = ListItemSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = ('id', 'item', 'auction_item_sold', 'auction_default_price', 'auction_status', 'auction_end_time', 'auction_winner')


"""serializer to create an auction: only owner of the item can create an auction"""


class CreateAuctionSerializer(ModelSerializer):
    class Meta:
        model = Auction
        fields = ('id', 'item', 'auction_default_price', 'auction_status', 'auction_end_time')

    def create(self, validated_data):
        answer, created = Auction.objects.update_or_create(item=validated_data.get('item', None),
                                                           defaults=validated_data)
        return answer


""" serializer for a winners of the auction: """


class WinnerSerializer(ModelSerializer):
    auction_winner = UserSerializer(read_only=True)
    item = ListItemSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = ('auction_winner', 'auction_end_time', 'item')