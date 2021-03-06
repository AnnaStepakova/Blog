# Generated by Django 3.1.5 on 2021-01-25 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_blogpost_snippet'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='header_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='snippet',
            field=models.CharField(max_length=250),
        ),
    ]
