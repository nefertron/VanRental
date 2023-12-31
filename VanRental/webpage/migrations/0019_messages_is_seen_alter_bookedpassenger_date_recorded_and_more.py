# Generated by Django 4.2.4 on 2023-09-08 05:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0018_rentedvan_travel_date_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='is_seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 8, 13, 15, 29, 131467)),
        ),
    ]
