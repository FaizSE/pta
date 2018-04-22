from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    filelocation = models.FileField(upload_to="csv_file/")
    created_at = models.DateTimeField(auto_now_add=True)