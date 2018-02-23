from django.shortcuts import render
from uploadcsv.models import File

def datalist(request):
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})