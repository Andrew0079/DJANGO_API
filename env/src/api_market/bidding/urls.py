from django.urls import path
from . import views

urlpatterns = [
    # path to view all bidders, with all the information: items, auction, users, bidders
    path('bidding/all', views.BiddingList.as_view(), name='all'),

    # path to create a bid
    path('bidding/create', views.CreateBid.as_view(), name='create'),

    # path to update or delete a specific bid by ID <-> pk
    path('bidding/<int:pk>/modify', views.GetUpdateDeleteBid.as_view(), name='modify'),

    # returning all the users and their bid associated with a specific auction based on auction ID <-> pk
    path('bidding/<int:pk>/bidders', views.AuctionListBidders.as_view(), name='bidders'),

    # path to get a sum of all bidders of a specific auction
    path('bidding/<int:pk>/sum', views.SumBidders.as_view(), name='sum'),
]
