from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from ..items.models import Item


class Auction(models.Model):
    OPEN = 'OPEN'
    PENDING = 'PENDING'
    CLOSED = 'CLOSED'
    STATUS = [(OPEN, 'OPEN'), (CLOSED, 'CLOSED'), (PENDING, 'PENDING')]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, default=None, db_column='item')
    auction_default_price = models.DecimalField(max_digits=19, decimal_places=2, default=0.00)
    auction_status = models.CharField(max_length=9, choices=STATUS, default=PENDING)
    auction_end_time = models.DateTimeField(default=now, auto_now=False, auto_now_add=False)
    auction_item_sold = models.BooleanField(default=False)
    auction_winner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.item.item_title

    class Meta:
        db_table = "auction"
