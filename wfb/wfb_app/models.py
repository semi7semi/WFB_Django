from django.db import models

class Units(models.Model):
    name = models.CharField(max_length=64, unique=True)
    offensive = models.IntegerField()
    strength = models.IntegerField()
    ap = models.IntegerField()
    reflex = models.BooleanField(default=False)


