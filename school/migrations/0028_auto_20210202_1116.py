# Generated by Django 3.1.1 on 2021-02-02 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0027_pumpapi'),
    ]

    operations = [
        migrations.CreateModel(
            name='bike_user',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('mobile_no', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('vechile_no', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('ssid', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('rf_id1', models.CharField(blank=True, max_length=64, null=True)),
                ('rf_id2', models.CharField(blank=True, max_length=64, null=True)),
                ('created_on', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('dealer', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='bikeapi',
            name='rf_id1',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='bikeapi',
            name='rf_id2',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
    ]
