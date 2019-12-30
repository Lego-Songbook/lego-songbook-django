from django.db import models

# Create your models here.


class Song(models.Model):
    """"""

    name = models.CharField(max_length=30)
    key = models.CharField(max_length=3, null=True)
    sheet_type = models.CharField(max_length=4, null=True)

    def __str__(self):
        return self.name


class Setlist(models.Model):
    """"""

    date = models.DateField()
    worship_leader = models.CharField(max_length=30)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return str(self.date)
