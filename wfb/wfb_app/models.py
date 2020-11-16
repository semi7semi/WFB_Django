from django.db import models


class Armys(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=64, unique=True)
    offensive = models.IntegerField()
    strength = models.IntegerField()
    ap = models.IntegerField()
    reflex = models.BooleanField(default=False)
    army = models.ForeignKey(Armys, on_delete=models.CASCADE, default=1)


class User(models.Model):
    login = models.CharField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    user_armies = models.ManyToManyField(Armys, through="UserArmies")


class UserArmies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    army = models.ForeignKey(Armys, on_delete=models.CASCADE)


GAME_RANK = (
    ("master", "Master"),
    ("local", "Local"),
    ("home", "Home")
)

OBJ = (
    (1, "Hold the Ground"),
    (2, "Breakthrough"),
    (3, "Spoils of War"),
    (4, "King of the Hill"),
    (5, "Capture the Flag"),
    (6, "Secure Target")
)

class Objectives(models.Model):
    name = models.IntegerField(choices=OBJ)


class GameResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    battle_points = models.IntegerField()
    objective = models.BooleanField(default=False)
    objective_type = models.ForeignKey(Objectives, on_delete=models.CASCADE)
    game_rank = models.CharField(max_length=16, choices=GAME_RANK)
    opponent = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)


