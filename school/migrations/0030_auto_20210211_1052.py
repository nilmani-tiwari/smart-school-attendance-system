# Generated by Django 3.1.1 on 2021-02-11 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0029_auto_20210204_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmaster',
            name='mobile',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]