# Generated by Django 3.1.1 on 2021-03-09 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0043_auto_20210309_1147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='school_machine_update',
            name='machine_state',
        ),
    ]
