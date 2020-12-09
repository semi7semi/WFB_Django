import pytest
# client i product - funkcje z conftest.py
from wfb_app.models import Units, Armys


@pytest.mark.django_db
def test_users_list(client):
    response = client.post("/users/")
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_unit(client):
    # sprawdzamy czy baza jest pusta
    assert len(Units.objects.all()) == 0
    # tworzymy obiekty
    army = Armys.objects.create(name="Warriors", short_name="WDG", description="Opis WDG")
    response = client.post("/add_unit/", {
        "name":"Barbarian",
        "offensive": 4,
        "strength": 3,
        "ap": 0,
        "reflex": False,
        "army": army.id
    })
    assert len(Units.objects.all()) == 1
    assert response.status_code == 302
    unit = Units.objects.get(name="Barbarian")
    assert unit.name == "Barbarian"
    assert unit.offensive == 4
    assert unit.strength == 3
    assert unit.ap == 0
    assert unit.reflex == False
    assert unit.army.name == "Warriors"

