# Generated by Django 3.0.8 on 2021-11-11 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0056_modelwithimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelwithimage',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='videos/', verbose_name=''),
        ),
    ]
