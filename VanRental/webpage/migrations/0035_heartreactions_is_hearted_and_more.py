# Generated by Django 4.2.4 on 2023-09-14 03:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0034_remove_tourcommentsection_is_hearted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='heartreactions',
            name='is_hearted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 942114)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 942114)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 943113)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 943113)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 939097)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 941109)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 14, 11, 33, 2, 943113)),
        ),
    ]
