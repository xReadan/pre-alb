from django.db import models

class Structures(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    rooms = models.IntegerField()
    image = models.TextField(null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE)