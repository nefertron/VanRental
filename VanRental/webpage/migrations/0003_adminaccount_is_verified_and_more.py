# Generated by Django 4.2.4 on 2023-08-05 13:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0002_alter_carpoolvan_date_recorded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminaccount',
            name='is_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='adminaccount',
            name='auth_token',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_cancelled',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_confirmed',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_dropped',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821)),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_rejected',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821), null=True),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821)),
        ),
        migrations.AlterField(
            model_name='driveraccount',
            name='auth_token',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821)),
        ),
        migrations.AlterField(
            model_name='passengeraccount',
            name='auth_token',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 5, 10, 4, 33, 513821)),
        ),
    ]