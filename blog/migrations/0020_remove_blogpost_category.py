# Generated by Django 3.1.5 on 2021-01-29 12:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0019_transfer_cats'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpost',
            name='category',
        ),
    ]
