from django.db import models

class NotificationRequest(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    structure = models.ForeignKey("structures.Structures", on_delete=models.CASCADE)

class NotificationList(models.Model):
    text = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    read = models.BooleanField()