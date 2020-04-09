from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    USED = 'USED'
    GOOD = 'GOOD'
    NEW = 'NEW'
    CONDITION = [(USED, 'USED'), (GOOD, 'GOOD'), (NEW, 'NEW')]

    item_owner = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    item_title = models.CharField(max_length=100)
    item_time_stamp = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    item_condition = models.CharField(max_length=4, choices=CONDITION, default=GOOD)
    item_description = models.CharField(max_length=100, default='')
    item_is_in_auction = models.BooleanField(default=False, editable=False)
    item_updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    item_image = models.ImageField('Uploaded image', null=True, blank=True, default='no image')

    def __str__(self):
        return self.item_title

    class Meta:
        db_table = "product_items"
