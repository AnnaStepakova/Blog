# Generated by Django 3.1.5 on 2021-01-29 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_auto_20210126_1147'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='category_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
    ]