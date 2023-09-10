# Generated by Django 4.2.4 on 2023-09-10 15:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0027_tourgallery_alter_bookedpassenger_date_recorded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourgallery',
            name='tour_gallery_id',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 249464)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 249464)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 250464)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 250464)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 247447)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 248446)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 59, 27, 250464)),
        ),
        migrations.AlterField(
            model_name='tourgallery',
            name='description',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='tourgallery',
            name='title',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
