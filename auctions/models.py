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
    user = models.ForeignKey(User, on_delete=models.CASCADE)# no guarda el id sino el user
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='NO')
    
    image = models.URLField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.FloatField()#starting big

    def __str__(self):
        return f"ARTICLE: {self.id}, NAME: {self.name}, SELLER: {self.user}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()
    #ahora si se la auction puedo saver los que han subastado
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='bidders', default=None)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    comment = models.TextField()

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="interested")

    def __str__(self):
        return f"Auction: {self.watchlist}, User:{self.user}"