# Generated by Django 4.1.5 on 2023-05-02 07:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0011_alter_notification_date_alter_reservation_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 2, 7, 8, 21, 777619)),
        ),
    ]
