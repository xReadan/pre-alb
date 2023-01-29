from django.db import models

class StructureRooms(models.Model):
    name = models.TextField()
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.TextField(null=True)
    structure = models.ForeignKey("structures.Structures", on_delete=models.CASCADE)
