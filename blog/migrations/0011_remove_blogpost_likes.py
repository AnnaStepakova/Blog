# Generated by Django 3.1.5 on 2021-01-24 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210124_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='likes',
        ),
    ]
