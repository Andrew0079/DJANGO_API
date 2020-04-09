from django.urls import path
from . import views

urlpatterns = [

    # return all Auction to any authenticated user
    path('auction/all', views.ListAllAuction.as_view(), name='all'),

    # authenticated user: create an Auction, User can only post his/her own item to an auction
    path('auction/create', views.CreateAuction.as_view(), name='create'),

    # authenticated user: can delete or update his/her own auction
    path('auction/<int:pk>/modify', views.GetUpdateDeleteAuction.as_view(), name='modify'),

    # OPEN,CLOSED,PENDING auctions e.g auction/OPEN
    path('auction/<slug:slug>/status', views.StatusAuctionList.as_view(), name='status'),

    # expired or new auctions e.g auction/expired or auction/new
    path('auction/<slug:slug>/type', views.NewOrExpiredAuctions.as_view(), name='type'),

    # returns auctions that expired and has a winner
    path('auction/winners', views.WinnersAuction.as_view(), name='winners'),

    # returns all the sold auctions
    path('auction/sold', views.SoldAuction.as_view(), name='sold'),
]

