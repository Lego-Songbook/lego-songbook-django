from django.db import models


class SongManager(models.Manager):
    def get_by_natural_key(self, name, key):
        return self.get(name=name, key=key)


class Song(models.Model):

    name = models.CharField(max_length=100)
    key = models.CharField(max_length=3, null=True)
    sheet_type = models.CharField(max_length=4, null=True)  # sheet file extension

    objects = SongManager()

    class Meta:
        unique_together = [["name", 'key']]

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name, self.key


class Person(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Instrument(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class InstrumentationManager(models.Manager):
    def get_by_natural_key(self, instrument, player):
        return self.get(instrument=instrument, player=player)


class Instrumentation(models.Model):

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    player = models.ForeignKey(Person, on_delete=models.CASCADE)

    objects = InstrumentationManager()

    def __str__(self):
        return f'{self.instrument} {self.player}'

    def natural_key(self):
        return self.instrument, self.player


class Setlist(models.Model):

    date = models.DateField()
    worship_leader = models.CharField(max_length=30)
    songs = models.ManyToManyField(Song)
    instrumentation = models.ManyToManyField(Instrumentation)

    def __str__(self):
        return str(self.date)
