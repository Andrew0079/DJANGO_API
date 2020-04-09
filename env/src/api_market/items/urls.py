from django.urls import path
from . import views

urlpatterns = [
    # authenticated user: return all available items to any user
    path('items/all', views.ListAllItems.as_view(), name='all'),

    # authenticated user: create item
    path('items/create', views.CreateItem.as_view(), name='created'),

    # authenticated user: updating/deleting a specific item, only the owner of the item can update or delete an item
    path('items/<int:pk>/modify', views.GetUpdateDeleteItem.as_view(), name='modify'),

    # authenticated user: display current user's items or any items that belong to other users e.g items/my_list or items/list
    path('items/<slug:slug>/', views.UserItemList.as_view()),

    # authenticated user: displays item based on the condition CONDITION: NEW, GOOD, USED
    path('items/<slug:slug>/condition', views.ItemsConditions.as_view(), name='condition'),

    # authenticated user: displays items either currently in auction or not
    path('items/<slug:slug>/auction', views.InAuctionItems.as_view(), name='auction'),

    # authenticated user: displays a specific user's items based on user id <-pk->
    path('items/<int:pk>/user_items', views.SpecUserItemList.as_view(), name='user_items'),

    # authenticated user: displays all items that are in auction associated with a specific user
    path('items/<int:pk>/user_in_auction', views.UserInAuctionItems.as_view(), name='user_in_auction'),
]
