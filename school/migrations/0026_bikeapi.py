# Generated by Django 3.1.1 on 2020-12-27 11:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_gpsrestapi'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bikeapi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('vechile_no', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('ssid', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('dealer', models.CharField(max_length=200)),
            ],
        ),
    ]
