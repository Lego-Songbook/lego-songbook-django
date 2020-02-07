# Generated by Django 3.0.3 on 2020-02-07 01:52

import datetime

from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ("songbook", "0007_auto_20200207_0916"),
    ]

    operations = [
        migrations.AddField(
            model_name="songattachment",
            name="file_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="songattachment",
            name="created",
            field=models.DateTimeField(
                blank=True,
                default=datetime.datetime(2020, 2, 7, 1, 52, 49, 30875, tzinfo=utc),
                null=True,
            ),
        ),
    ]