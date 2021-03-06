# Generated by Django 3.2.6 on 2021-09-15 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuctionList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('ELE', 'Electronica'), ('CO', 'Cocina'), ('RP', 'Ropa'), ('HG', 'Higiene'), ('NO', 'No category')], max_length=100)),
                ('image', models.URLField()),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('bid', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
