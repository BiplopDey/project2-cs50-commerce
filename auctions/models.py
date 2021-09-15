from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionList(models.Model):
    CATEGORY_CHOICES = [
    ('ELE','Electronica'),
    ('CO','Cocina'),
    ('RP','Ropa'),
    ('HG','Higiene'),
    ('NO', 'No category')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    
    image = models.URLField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.FloatField()#starting big