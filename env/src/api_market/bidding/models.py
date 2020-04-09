from django.db import models
from django.contrib.auth.models import User
from ..auction.models import Auction

"""Bidding model contains TWO foreign keys: Auction id and User id"""


class Bidding(models.Model):
    bidding_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='bidding_user')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default=None, db_column='auction')
    bidding_price = models.DecimalField(max_digits=19, decimal_places=4, default=0.0000)

    def __str__(self):
        return self.auction.item.item_title

    class Meta:
        db_table = "auction_bidders"
        ordering = ['-bidding_price']
