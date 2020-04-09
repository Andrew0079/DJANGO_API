from .models import Item
from .serializers import ListItemSerializer, CreateItemSerializer
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from django.http import Http404
from rest_framework.response import Response
from django.db.models import Q

"""Create Api View: authenticated  users can create items """


class CreateItem(CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = CreateItemSerializer


"""List Api View: authenticated  users can view items """


class ListAllItems(ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ListItemSerializer


"""Retrieve Update Destroy APIView: authenticated  user can update, delete his/her own item """


class GetUpdateDeleteItem(RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ListItemSerializer

    """Get specific item based on item ID <-> pk"""

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    """Updating a specific item. Only user who owns the item can perform an update. """

    def update(self, request, *args, **kwargs):

        # global variable to get the owner id of the item
        item_owner_id = None
        # check if item is exist, otherwise  an error is returned
        try:
            self.object = self.get_object()
            item_owner_id = self.get_serializer(self.object)
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_201_CREATED

        # check if the request user is the owner of the item
        if int(request.user.id) != int(item_owner_id.data['item_owner']['id']):
            return Response("You do not own this item. You can only modify your own item.")

        # saving updated item's details, and returning the data
        serializer = self.get_serializer(self.object, data=request.data)
        if serializer.is_valid():
            self.object = serializer.save()
            return Response(serializer.data, status=success_status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """Deleting an item: Only the owner of the item can perform a delete action."""

    def delete(self, request, *args, **kwargs):
        # global variable for later use(assigment) it will contain the owner id of the item
        item_owner_id = None
        # checking if item exist
        try:
            self.object = self.get_object()
            item_owner_id = self.get_serializer(self.object)
            success_status_code = status.HTTP_200_OK
        except Http404:
            success_status_code = status.HTTP_201_CREATED

        # check if request user is the owner of the item, if not an error message is returned
        if int(request.user.id) != int(item_owner_id.data['item_owner']['id']):
            return Response("You do not own this item. You can only delete your own item.",
                            status=status.HTTP_400_BAD_REQUEST)
        # deleting item from database, returning success message
        self.object.delete()
        return Response("Item successfully deleted.", status=success_status_code)


""" This view either returns a list of all the items of the currently authenticated user.
    or items of the other users"""


class UserItemList(ListAPIView):
    serializer_class = ListItemSerializer

    def get_queryset(self):
        if self.kwargs['slug'] == 'my_list':
            return Item.objects.filter(item_owner=self.request.user)
        elif self.kwargs['slug'] == 'list':
            return Item.objects.filter(~Q(item_owner=self.request.user))


# view to return items based on a condition CONDITION: NEW, GOOD, USED
class ItemsConditions(ListAPIView):
    serializer_class = ListItemSerializer

    def get_queryset(self):
        if self.kwargs['slug'] == 'new':
            return Item.objects.filter(item_condition="NEW")
        elif self.kwargs['slug'] == 'good':
            return Item.objects.filter(item_condition="GOOD")
        elif self.kwargs['slug'] == 'used':
            return Item.objects.filter(item_condition="USED")


# view to return items currently in auction or not
class InAuctionItems(ListAPIView):
    serializer_class = ListItemSerializer

    def get_queryset(self):
        if self.kwargs['slug'] == 'in_auction':
            return Item.objects.filter(item_is_in_auction=True)
        elif self.kwargs['slug'] == 'not_in_auction':
            return Item.objects.filter(item_condition=False)


# view to return a specific user's items
class SpecUserItemList(ListAPIView):
    serializer_class = ListItemSerializer

    def get_queryset(self):
        return Item.objects.filter(item_owner=int(self.kwargs['pk']))


# view to return items currently in auction or not
class UserInAuctionItems(ListAPIView):
    serializer_class = ListItemSerializer

    def get_queryset(self):
        return Item.objects.filter(item_is_in_auction=True, item_owner=self.kwargs['pk'])