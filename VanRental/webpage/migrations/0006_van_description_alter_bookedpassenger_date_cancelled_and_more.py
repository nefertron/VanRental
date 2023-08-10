# Generated by Django 4.2.4 on 2023-08-10 03:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0005_remove_van_vehicle_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='van',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_cancelled',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_confirmed',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_dropped',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934), null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934)),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_rejected',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934), null=True),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 10, 11, 13, 40, 84934)),
        ),
    ]