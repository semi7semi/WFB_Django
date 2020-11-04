from django.db import models

class Units(models.Model):
    name = models.CharField(max_length=64, unique=True)
    offensive = models.IntegerField()
    strength = models.IntegerField()
    ap = models.IntegerField()
    reflex = models.BooleanField(default=False)

class Armys(models.Model):
    name = models.CharField(max_length=54, unique=True)
    description = models.CharField(max_length=255)
    


