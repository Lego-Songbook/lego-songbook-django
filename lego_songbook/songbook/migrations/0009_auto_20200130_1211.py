# Generated by Django 3.0.1 on 2020-01-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("songbook", "0008_team_positions"),
    ]

    operations = [
        migrations.RemoveField(model_name="person", name="_nickname",),
        migrations.AddField(
            model_name="person",
            name="nickname",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="birthday",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="gender",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="last_name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="person",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="position",
            name="people",
            field=models.ManyToManyField(
                blank=True, related_name="positions", to="songbook.Person"
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="positions",
            field=models.ManyToManyField(
                blank=True, related_name="teams", to="songbook.Position"
            ),
        ),
    ]
