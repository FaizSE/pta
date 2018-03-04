from django.db import models
from django.forms import ModelForm

class File(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)
    filename = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Upload(models.Model):
    pic = models.FileField(upload_to="images/")
    upload_date=models.DateTimeField(auto_now_add =True)

# FileUpload form class.
class UploadForm(ModelForm):
    class Meta:
        model = Upload
        fields = ('pic',)