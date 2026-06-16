from django.db import models


class Role(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class User(models.Model):

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.username