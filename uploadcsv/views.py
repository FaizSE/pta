from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import pandas as pd


def viewcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'viewcsv.html', {'file': file})

def opencsv(request, pk):

    mperson = get_object_or_404(File, pk=pk).name

    csvfile=settings.MEDIA_ROOT + '/' + mperson
    data = pd.read_csv(csvfile, encoding = "ISO-8859-1")
    data_html = data.to_html()
    context = {'loaded_data': data_html}
    return render(request, 'opencsv.html', context)

def newcsv(request):
    if request.method == 'POST':

        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('newcsv'))

    else:
        img = UploadForm()

    return render(request, 'newcsv.html',{'form':img})