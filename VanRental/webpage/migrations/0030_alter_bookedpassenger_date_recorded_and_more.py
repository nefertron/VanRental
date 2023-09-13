# Generated by Django 4.2.4 on 2023-09-13 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0029_alter_bookedpassenger_date_recorded_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 43288)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 43288)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 45291)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 45291)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 41290)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 42289)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 13, 22, 29, 39, 44287)),
        ),
        migrations.AlterField(
            model_name='tourgallery',
            name='is_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
