from django.db import models

class Structures(models.Model):
    # Basic infos
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rooms = models.IntegerField()
    image = models.TextField(null=True)
    description = models.TextField(null=True)
    # Services
    restaurants = models.BooleanField(default=False)
    pool = models.BooleanField(default=False)
    spa = models.BooleanField(default=False)
    # Owner
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)