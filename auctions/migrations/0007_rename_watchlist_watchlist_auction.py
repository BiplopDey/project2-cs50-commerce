# Generated by Django 3.2.6 on 2021-09-25 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_bid_auction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='watchlist',
            old_name='watchlist',
            new_name='auction',
        ),
    ]