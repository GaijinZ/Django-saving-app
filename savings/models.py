from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    objects = models.Manager()

    def __str__(self):
        return self.user.username


class YourGoal(models.Model):
    date = models.DateField(default=datetime.now)
    cel = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = models.Manager()


class Outgoings(models.Model):
    date = models.DateField(default=datetime.now)
    kategoria = models.TextField(max_length=20)
    suma = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.kategoria

    class Meta:
        db_table = "outgoings"


class MoneyBox(models.Model):
    date = models.DateField(default=datetime.now)
    wolumen = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = models.Manager()


class Obligations(models.Model):
    date = models.DateField(default=datetime.now)
    kategoria = models.TextField(max_length=20)
    kwota = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    objects = models.Manager()

    def __str__(self):
        return self.kategoria
