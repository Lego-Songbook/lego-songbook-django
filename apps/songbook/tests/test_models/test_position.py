import pytest

from ...models import Team, Position, Person

django_db = pytest.mark.django_db


@django_db
def test_position_string_representation_without_team():
    p = Position(name="Guitarist")
    p.save()
    assert str(p) == p.name == "Guitarist"


@django_db
def test_position_string_representation_with_team():
    t = Team(name="Worship Team")
    t.save()
    p = Position(name="Guitarist", team=t)
    p.save()
    assert str(p) == "Guitarist (Worship Team)"


@django_db
def test_get_all_people_in_a_position():
    p1 = Person(first_name="John")
    p2 = Person(first_name="Peter")
    p1.save()
    p2.save()
    pos = Position(name="Guitarist")
    pos.save()

    pos.people.add(p1, p2)
    all_guitarists = [str(x) for x in pos.people.all()]

    assert all_guitarists == ["John", "Peter"]
