from django.db import models

class Notifications(models.Model):
    message = models.CharField(max_length=264)
    is_read = models.BooleanField()