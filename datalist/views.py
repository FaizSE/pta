import os
from django.conf import settings
from uploadcsv.models import File
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse



def datalist(request):
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})

def deletedata(request,pk):
    files = get_object_or_404(File, pk=pk)
    files.delete()
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})

def downloaddata(request, pk):
    filelocation = str(get_object_or_404(File, pk=pk).filelocation)
    path=settings.MEDIA_ROOT + '/' + filelocation
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})
