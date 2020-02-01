import pytest

from ...models import Person

from datetime import date

django_db = pytest.mark.django_db


@django_db
def test_full_name_without_a_last_name():
    p = Person.objects.create(first_name="John")
    assert str(p) == "John"


@django_db
def test_full_name_chinese():
    p = Person.objects.create(last_name="张", first_name="三")
    assert str(p) == "张三"


@django_db
def test_full_name_in_english():
    p = Person.objects.create(last_name="Bryant", first_name="Kobe")
    assert str(p) == "Kobe Bryant"


@django_db
def test_default_nickname():
    p = Person(first_name="John")
    p.save()

    assert p.nickname == "John"


@django_db
def test_setting_nickname():
    p = Person(first_name="John", nickname="Johnny")
    p.save()

    assert p.nickname == "Johnny"


@django_db
def test_age_calculation():
    p = Person(first_name="John", birthday=date(1990, 1, 1))
    p.save()

    assert p.age == 30  # as of 2020
