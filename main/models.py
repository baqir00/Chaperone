from django.db import models
from django.contrib.auth.models import User


# Create your models here.





class Result(models.Model):
    username = models.ForeignKey(User, on_delete=None, primary_key=True)
    mba = models.IntegerField(default=0)
    mtech = models.IntegerField(default=0)
    mbawe = models.IntegerField(default=0)
    govt = models.IntegerField(default=0)
    priv = models.IntegerField(default=0)
    bank = models.IntegerField(default=0)
    civil = models.IntegerField(default=0)
    entre = models.IntegerField(default=0)
    ms = models.IntegerField(default=0)

    def __str__(self):
        return self.username.username
