# Generated by Django 4.2.4 on 2023-09-10 15:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webpage', '0026_faqs_getintouch_alter_bookedpassenger_date_recorded_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TourGallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('title', models.TextField()),
                ('is_enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 378165)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 378165)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 379165)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 379165)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 376166)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 377166)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 10, 23, 54, 40, 379165)),
        ),
        migrations.CreateModel(
            name='TourGalleryImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.TextField()),
                ('is_enabled', models.BooleanField(default=True)),
                ('tour_gallery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.tourgallery')),
            ],
        ),
        migrations.AddField(
            model_name='tourgallery',
            name='rented_van',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.rentedvan'),
        ),
    ]
