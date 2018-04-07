from django.shortcuts import render
from .models import UploadForm, File
from django.http import HttpResponseRedirect
from django.urls import reverse

from urllib.request import urlretrieve
from django.conf import settings
import pandas as pd

def newcsv(request):
    if request.method == 'POST':

        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('newcsv'))

        else:
            name = request.POST['name']
            description = request.POST['description']
            url = request.POST['url']
            renamefile = request.POST['renamefile'] + '.csv'
            urlretrieve(url, renamefile)# Save file locally
            df = pd.read_csv(renamefile, encoding = "ISO-8859-1")
            filelocation='/csv_file/' + renamefile
            csvfile = settings.MEDIA_ROOT + '/csv_file/' + renamefile
            df.to_csv(csvfile, encoding="ISO-8859-1", index=False)
            File.objects.create(name=name, description=description,filelocation=filelocation)
            return HttpResponseRedirect(reverse('newcsv'))

    else:
        form = UploadForm()

    return render(request, 'uploadcsv/uploadcsv.html',{'form':form,})