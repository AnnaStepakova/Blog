# Generated by Django 3.1.5 on 2021-01-24 11:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0011_remove_blogpost_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='likes',
            field=models.ManyToManyField(related_name='blogposts', to=settings.AUTH_USER_MODEL),
        ),
    ]
