# Generated by Django 3.2 on 2021-08-09 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20210808_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='alt_image',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='alt_image',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
