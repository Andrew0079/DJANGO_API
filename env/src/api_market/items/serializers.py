from rest_framework.serializers import ModelSerializer
from .models import Item
from oAuth2Server.serializers import UserSerializer

''' serializer of the Item ORM'''


class ListItemSerializer(ModelSerializer):
    item_owner = UserSerializer(read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'item_owner', 'item_title', 'item_description',
                  'item_is_in_auction', 'item_condition', 'item_time_stamp', 'item_updated', 'item_image')
        read_only_fields = ('item_time_stamp', 'item_is_in_auction')


class CreateItemSerializer(ModelSerializer):

    class Meta:
        model = Item
        fields = ('id', 'item_owner', 'item_title', 'item_description', 'item_is_in_auction',
                  'item_condition', 'item_time_stamp', 'item_updated', 'item_image')
        read_only_fields = ('item_time_stamp', 'item_is_in_auction')
