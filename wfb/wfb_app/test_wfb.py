import pytest
from django.contrib.auth.models import User
from wfb_app.models import Units, Armys, Objectives, GameResults
from datetime import datetime

@pytest.mark.django_db
def test_users_list(client, user):
    response = client.post("/users/")
    assert response.status_code == 302
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_users_details(client, user):
    response = client.post(f"/user_details/{user.pk}")
    assert response.status_code == 301


# @pytest.mark.django_db
# def test_add_user(client):
#     # sprawdzamy czy baza jest pusta
#     assert len(User.objects.all()) == 0
#     # tworzymy obiekty
#     army = Armys.objects.create(name="Warriors", short_name="WDG", description="Opis WDG")
#     response = client.post("/add_user/", {
#         "username": "Marcin",
#         "password": "1234",
#         "password_2": "1234",
#         "email": "aa@aa.pl",
#         "user_army": army.id
#     })
#     assert len(User.objects.all()) == 1
#     assert response.status_code == 200
#     user = User.objects.get(username="Marcin")
#     assert user.username == "Marcin"
#     assert user.password == "1234"
#     assert user.email == "aa@aa.pl"
#     assert user.army.name == "Warriors"


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


@pytest.mark.django_db
def test_add_result(client, user):
    assert len(GameResults.objects.all()) == 0
    objective = Objectives.objects.create(name="King of the Hill")
    response = client.post("/ranking/add_result/", {
        "user": user.id,
        "battle_points": 10,
        "objective": True,
        "objective_type": objective,
        "game_rank": "master",
        "opponent": "Przeciwnik",
        "date": datetime.now()
    })
    assert len(GameResults.objects.all()) == 1
    assert response.status_code == 302
    result = GameResults.objects.get(user=user.name)
    assert result.battle_points == 10
    assert result.objective_type == "King of the Hill"
    assert result.date == datetime.now()