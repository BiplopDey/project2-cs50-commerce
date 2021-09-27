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
    values=[i[0] for i in CATEGORY_CHOICES]

    user = models.ForeignKey(User, on_delete=models.CASCADE)# no guarda el id sino el user
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='NO')
    
    image = models.URLField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.FloatField()#starting big
    date = models.DateTimeField() # hay que importrar datetime, y luego se pone datetime.datetime.now()
    # y salen el tiempo hasta en segundos
    closed = models.BooleanField(default=False)
    def __str__(self):
        return f"ARTICLE: {self.id}, NAME: {self.name}, SELLER: {self.user}"

class Bid(models.Model):#guarda al mejor postor
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField()#current_bid
    #ahora si se la auction puedo saver los que han subastado
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name='bidders', default=None)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    date = models.DateTimeField() # hay que importrar datetime, y luego se pone datetime.datetime.now()
    # y salen el tiempo hasta en segundos
    class Meta:
        ordering = ['date']
        indexes = [
            models.Index(fields=['auction', 'date']),
            models.Index(fields=['date']),
        ]

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="interested")

    def __str__(self):
        return f"Auction: {self.auction}, User:{self.user}"