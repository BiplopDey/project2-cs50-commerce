# Generated by Django 3.2.6 on 2021-09-15 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlist',
            name='category',
            field=models.CharField(choices=[('ELE', 'Electronica'), ('CO', 'Cocina'), ('RP', 'Ropa'), ('HG', 'Higiene'), ('NO', 'No category')], default='NO', max_length=100),
        ),
    ]
