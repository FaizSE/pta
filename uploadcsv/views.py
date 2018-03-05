from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def uploadcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'uploadcsv.html', {'file': file})

def newcsv(request):
    if request.method == 'POST':

        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('newcsv'))

    else:
        img = UploadForm()

    return render(request, 'newcsv.html',{'form':img})