# Generated by Django 3.0.1 on 2020-01-30 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("songbook", "0010_auto_20200130_1239"),
    ]

    operations = [
        migrations.AddField(
            model_name="arrangement",
            name="key",
            field=models.CharField(default="C", max_length=10),
        ),
    ]
