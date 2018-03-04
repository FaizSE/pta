from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm, Upload
from django.http import HttpResponseRedirect
from django.urls import reverse

def uploadcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'uploadcsv.html', {'file': file})

def newcsv(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']



        file=File.objects.create(
            name=name,
            description=description,

        )

        img = UploadForm(request.POST, request.FILES)
        if img.is_valid():
            img.save()
            return HttpResponseRedirect(reverse('newcsv'))

    else:
        img = UploadForm()

    return render(request, 'newcsv.html',{'form':img})