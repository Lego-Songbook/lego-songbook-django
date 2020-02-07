"""
Songbook models.

``ServiceType`` is the top-level model.

"""
import re
from datetime import date

from django.db import models
from django.utils import text, timezone


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


# class SongManager(models.Manager):
#     """Make 'name' and 'key' combined unique."""
#
#     def get_by_natural_key(self, name, original_key):
#         return self.get(name=name, original_key=original_key)


class Song(models.Model):

    title = models.CharField(max_length=100)
    key = models.CharField(max_length=3, null=True, blank=True)
    bpm = models.IntegerField(verbose_name="BPM", null=True, blank=True)
    meter = models.CharField(max_length=20, null=True, blank=True)
    # objects = SongManager()

    def __str__(self):
        return self.name

    # def natural_key(self):  # ???
    #     return self.name, self.key


def song_attachment_path(instance, filename):
    """
    Helper function for determining the upload path of a file.
    :param instance: a SongAttachment instance
    :param filename: the original name of the uploaded file. This value
        is ignored, since we are using the user specified file name as
        the real file name.
    :return:
    """
    # file will be uploaded to MEDIA_ROOT/songs/<media_type>/<song_name>
    song_title_slug = text.slugify(instance.song.title)
    if instance.file_name is None:
        file_name = filename
    else:
        file_name = instance.file_name
    return f"songbook/{instance.media_type}/{song_title_slug}/{file_name}"


class SongAttachment(models.Model):
    """
    The attachments of a song arrangement.
    """

    class MediaType(models.TextChoices):
        AUDIO = "audio", "Audio File"
        SHEET = "sheet", "Music Sheet"

    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="attachments")
    media_type = models.CharField(max_length=64, choices=MediaType.choices)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    main = models.BooleanField(
        help_text=(
            "Whether or not that this attachment should be listed as the main"
            "attachment on a song list view."
        ),
        default=True,
    )
    attachment = models.FileField(upload_to=song_attachment_path)
    created = models.DateTimeField(default=timezone.now(), null=True, blank=True)


class Plan(models.Model):
    """
    A service plan, containing a detailed worship info.
    """

    date = models.DateField()
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True)
    songs = models.ManyToManyField(Song, related_name="plans")
    team_arrangement = models.ForeignKey(
        TeamArrangement, on_delete=models.CASCADE, related_name="plans", null=True
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_type} ({self.date})"

    @property
    def upcoming(self):
        """
        Determine if the plan is an upcoming plan or not.
        :return: bool
        """
        return date.today() < self.date
