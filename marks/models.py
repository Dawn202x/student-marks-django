from django.db import models
from django.contrib.auth.models import User

class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marks")
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    pin_code = models.CharField(max_length=4)