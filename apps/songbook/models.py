"""
Songbook models.

``ServiceType`` is the top-level model.

"""
import re
from datetime import date

from django.db import models


class ServiceType(models.Model):
    """
    A class of service, such as a Sunday Service or a Friday Small
    Group.
    """

    name = models.CharField(max_length=100)
    recurrence = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class ServiceTime(models.Model):
    """
    A particular time of which the service happens.
    """

    date = models.DateField()
    starting_time = models.TimeField()
    stopping_time = models.TimeField()
    service = models.ForeignKey(
        ServiceType, on_delete=models.CASCADE, related_name="service_times"
    )

    def __str__(self):
        return f"{self.date}, {self.starting_time} to {self.stopping_time}"


class Team(models.Model):
    """
    A group of people that has a particular job, e.g. Worship Team,
    Media Team, etc.

    A team has a list of positions, and each position contains a pool
    of team members in the team. For example, in a Worship Team,
    there is a worship leader, a keyboardist, a guitarist, and a
    drummer, and there are three people in the worship leader position,
    who take turns to lead worship every week.

    Different Service Types have different teams, and the team members
    are all different.

    Each service type has many teams.
    """

    name = models.CharField(max_length=50)
    service_type = models.ForeignKey(
        ServiceType, on_delete=models.CASCADE, related_name="teams", null=True,
    )

    def __str__(self):
        return self.name


class Person(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        if self.localization == "zh":
            return f"{self.last_name or ''}{self.first_name}"  # zh dialect
        else:
            return (
                f"{self.first_name}"
                f"{'' if self.last_name is None else ' ' + self.last_name}"
            )

    @property
    def localization(self):
        if re.findall(r"[\u4e00-\u9fff]+", self.first_name):
            return "zh"
        else:
            return "en"

    @property
    def age(self):
        if self.birthday is not None:
            born = self.birthday
            today = date.today()
            return (
                today.year
                - born.year
                - ((today.month, today.day) < (born.month, born.day))
            )

    @property
    def all_positions(self):
        return [str(x) for x in self.positions.all()]

    def save(self, *args, **kwargs):
        """
        If the nickname is not given, set it to the person's first name.
        """
        if self.nickname is None:
            self.nickname = self.first_name
        super().save(*args, **kwargs)


class Position(models.Model):
    """
    A position in a team.

    A position has many people, and each person can serve in many
    positions. A team has many positions, but each position should only
    be tied to one team.
    """

    name = models.CharField(max_length=50)
    team = models.ForeignKey(
        Team, related_name="positions", on_delete=models.CASCADE, null=True
    )
    people = models.ManyToManyField(Person, related_name="positions", blank=True)

    def __str__(self):
        if self.team is None:
            return self.name
        else:
            return f"{self.name} ({self.team})"


class PositionAssignment(models.Model):  # Need a better name.
    """
    A particular combination of a position and a person. This model
    is used in ``Plan`` model.
    """

    class AssignmentStatus(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        UNCONFIRMED = "unconfirmed", "Unconfirmed"
        DECLINED = "declined", "Declined"

    status = models.CharField(
        max_length=16,
        default=AssignmentStatus.UNCONFIRMED,
        choices=AssignmentStatus.choices,
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE,)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["position", "person"], name="unique_assignment",
            )
        ]

    def __str__(self):
        return f"{self.position}: {self.person}"


class TeamArrangement(models.Model):
    """
    A list of position arrangements.
    """

    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    position_assignments = models.ManyToManyField(
        to=PositionAssignment, related_name="team_arrangements",
    )

    def __str__(self):
        return f"{self.team} Arrangement ({id(self)})"


class SongManager(models.Manager):
    """Make 'name' and 'key' combined unique."""

    def get_by_natural_key(self, name, original_key):
        return self.get(name=name, original_key=original_key)


class Song(models.Model):

    name = models.CharField(max_length=100)
    original_key = models.CharField(max_length=3, null=True, blank=True)
    # sheet_type = models.CharField(max_length=4, null=True, blank=True)
    objects = SongManager()

    def __str__(self):
        return self.name

    def natural_key(self):  # ???
        return self.name, self.original_key


class SongArrangement(models.Model):
    """
    A particular arrangement of a song.
    """

    title = models.CharField(max_length=100, default="Default Arrangement")
    song = models.ForeignKey(
        Song, on_delete=models.CASCADE, related_name="song_arrangements"
    )
    key = models.CharField(max_length=10, null=True, blank=True)
    length = models.CharField(max_length=20, null=True, blank=True)
    bpm = models.IntegerField(verbose_name="BPM", null=True, blank=True)
    meter = models.CharField(max_length=20, null=True, blank=True)
    sequence = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.song.name} ({self.title})"

    def save(self, *args, **kwargs):
        original_key = self.song.original_key
        if self.key is None and original_key is not None:
            self.key = original_key
        super().save(*args, **kwargs)


class Plan(models.Model):
    """
    A service plan, containing a detailed worship info.
    """

    date = models.DateField()
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True)
    song_arrangements = models.ManyToManyField(SongArrangement, related_name="plans")
    team_arrangement = models.ManyToManyField(TeamArrangement, related_name="plans")

    def __str__(self):
        return f"{self.service_type} ({self.date})"


class Setlist(models.Model):

    date = models.DateField()
    worship_leader = models.CharField(max_length=30)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return str(self.date)
