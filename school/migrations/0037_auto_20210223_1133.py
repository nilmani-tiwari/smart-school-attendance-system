# Generated by Django 3.1.1 on 2021-02-23 11:33

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0036_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=0, size=[640, 480], upload_to='images/'),
        ),
    ]
