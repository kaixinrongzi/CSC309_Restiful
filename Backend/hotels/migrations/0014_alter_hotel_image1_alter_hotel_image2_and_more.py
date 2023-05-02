# Generated by Django 4.1.5 on 2023-05-02 08:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0013_hotel_image1_hotel_image2_hotel_image3_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='image1',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image2',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='image3',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 8, 19, 16, 931079)),
        ),
    ]
