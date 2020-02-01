import pytest
from django.db.utils import IntegrityError

from ...models import Person, Position, PositionAssignment

django_db = pytest.mark.django_db


@django_db
def test_get_all_positions_of_a_person():
    p = Person(first_name="John")
    p.save()
    pos1 = Position(name="Guitarist")
    pos2 = Position(name="Keyboardist")
    pos1.save()
    pos2.save()
    p.positions.add(pos1, pos2)

    assert list(p.positions.all()) == [pos1, pos2]


@django_db
def test_default_status():
    p = Person.objects.create(first_name="John")
    pos = Position.objects.create(name="Guitarist")
    pos_assign = PositionAssignment.objects.create(position=pos, person=p)

    assert pos_assign.status == "unconfirmed"


@django_db
def test_person_position_unique_together():
    p = Person.objects.create(first_name="John")
    pos = Position.objects.create(name="Guitarist")
    PositionAssignment.objects.create(position=pos, person=p)

    with pytest.raises(IntegrityError):
        PositionAssignment.objects.create(position=pos, person=p)
