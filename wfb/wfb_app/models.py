from django.db import models

class Armys(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=255)

class Units(models.Model):
    name = models.CharField(max_length=64, unique=True)
    offensive = models.IntegerField()
    strength = models.IntegerField()
    ap = models.IntegerField()
    reflex = models.BooleanField(default=False)
    army = models.ForeignKey(Armys, on_delete=models.CASCADE, default=1)



    


