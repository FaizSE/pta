from django.shortcuts import render
from .models import UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse


def newcsv(request):
    if request.method == 'POST':

        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('newcsv'))

    else:
        img = UploadForm()

    return render(request, 'uploadcsv/uploadcsv.html',{'form':img})

