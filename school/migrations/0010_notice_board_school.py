# Generated by Django 3.0.2 on 2020-08-22 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0009_delete_notice_board_school'),
    ]

    operations = [
        migrations.CreateModel(
            name='notice_board_school',
            fields=[
                ('notice_id', models.AutoField(primary_key=True, serialize=False)),
                ('school_code', models.CharField(blank=True, max_length=200, null=True)),
                ('Title', models.CharField(blank=True, max_length=64, null=True)),
                ('Details', models.CharField(blank=True, max_length=64, null=True)),
                ('Posted_by', models.CharField(blank=True, max_length=64, null=True)),
                ('Date', models.DateField(null=True)),
            ],
        ),
    ]