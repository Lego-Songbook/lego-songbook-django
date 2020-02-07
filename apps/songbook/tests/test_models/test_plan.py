from datetime import date

import pytest

from ...models import Plan

django_db = pytest.mark.django_db


@django_db
def test_upcoming_plan():
    p = Plan.objects.create(date=date(2000, 1, 1))
    assert p.upcoming is False


@django_db
def test_not_an_upcoming_plan():
    p = Plan.objects.create(date=date(2099, 12, 31))
    assert p.upcoming is True


@django_db
def test_upcoming_plan_excluding_today():
    p = Plan.objects.create(date=date.today())
    assert p.upcoming is False
