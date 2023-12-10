# Generated by Django 4.2.4 on 2023-12-10 06:33

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webpage', '0039_tourgallery_tour_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookedpassenger',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 114004)),
        ),
        migrations.AlterField(
            model_name='carpoolvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 113005)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_seen',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 115004)),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date_sent',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 115004)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 112005)),
        ),
        migrations.AlterField(
            model_name='rentedvan',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 113005)),
        ),
        migrations.AlterField(
            model_name='review',
            name='date_recorded',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 115004)),
        ),
        migrations.AlterField(
            model_name='tourcommentsection',
            name='date_commented',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 118004)),
        ),
        migrations.CreateModel(
            name='VanReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=5)),
                ('comment', models.TextField()),
                ('date_recorded', models.DateTimeField(default=datetime.datetime(2023, 12, 10, 14, 33, 49, 115004))),
                ('review_id', models.CharField(max_length=30)),
                ('reviewed_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('van', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webpage.van')),
            ],
        ),
    ]