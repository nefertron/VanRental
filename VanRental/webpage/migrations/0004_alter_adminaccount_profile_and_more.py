# Generated by Django 4.2.4 on 2023-08-05 13:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0003_adminaccount_is_verified_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminaccount',
            name='profile',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_cancelled',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_confirmed',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_dropped',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371)),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_rejected',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371), null=True),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 6, 9, 816671)),
        ),
        migrations.AlterField(
            model_name='driveraccount',
            name='profile',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 6, 9, 816671)),
        ),
        migrations.AlterField(
            model_name='passengeraccount',
            name='profile',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 6, 9, 816671)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 6, 9, 832371)),
        ),
    ]
