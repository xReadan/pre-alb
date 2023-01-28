from django.db import models

class Reservations(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    structure = models.ForeignKey("structures.Structures", on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()
