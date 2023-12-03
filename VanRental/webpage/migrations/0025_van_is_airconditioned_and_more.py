# Generated by Django 4.2.4 on 2023-09-10 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0024_rentedvan_pick_up_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='van',
            name='is_airconditioned',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 317557)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 316557)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 318557)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 318557)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 315558)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 316557)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 14, 25, 20, 317557)),
        ),
    ]