# Generated by Django 3.1.5 on 2021-01-25 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20210125_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='snippet',
            field=models.CharField(default='Empty snippet', max_length=250),
        ),
    ]