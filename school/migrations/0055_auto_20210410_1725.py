# Generated by Django 3.1.5 on 2021-04-10 11:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0054_auto_20210410_1649'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='attendance_api',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='attendance_api',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='bike_user',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bike_user_details',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='bikeapi',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='busapi',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='busmap',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='classmaster',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='divisionmaster',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='gpsrestapi',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='gpsrestapi',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='mediummaster',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='message_pack',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='message_pack',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='notice_board_school',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='posts',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='pumpapi',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='pumpapi',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='quary_form',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_holiday',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_library',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_machine_api',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_machine_details',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_machine_update',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_transport',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='school_transport',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='user_command',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='user_command',
            name='created_on',
        ),
        migrations.AlterField(
            model_name='classmaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='divisionmaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='mediummaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='notice_board_school',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='ownermaster',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ownermaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='parentsmaster',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='parentsmaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='quary_form',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='school_holiday',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='school_library',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='schoolmaster',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolmaster',
            name='created_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='staffmaster',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmaster',
            name='created_by',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmaster',
            name='created_on',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]