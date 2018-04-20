from django.db import models
from django.forms import ModelForm

class File(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    filelocation = models.FileField(upload_to="csv_file/")
    created_at = models.DateTimeField(auto_now_add=True)