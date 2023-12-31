# Generated by Django 4.2.4 on 2023-12-03 04:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0036_tourcommentsection_date_commented_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='van',
            name='color_coding',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 963330)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 962328)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 965330)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 965330)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 959329)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 960326)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 964331)),
        ),
        migrations.AlterField(
            model_name='tourcommentsection',
            name='date_commented',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 3, 12, 41, 30, 971091)),
        ),
    ]
