from django.shortcuts import render
from .models import File
from django.http import HttpResponseRedirect
from django.urls import reverse

from urllib.request import urlretrieve
from django.conf import settings
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



@login_required(login_url='login')

def newcsv(request):
    if request.method == 'POST':
            name = request.POST['name']
            description = request.POST['description']
            via=request.POST['via']
            userinstance=User.objects.get(id=request.user.id)
            renamefile = name + '.csv'

            try:
                if via == 'selecturl':#Upload via URL
                    url = request.POST['url']
                    csvfile = settings.MEDIA_ROOT + '/csv_file/' + renamefile
                    urlretrieve(url, csvfile)# Save file locally
                    df = pd.read_csv(csvfile, encoding = "ISO-8859-1")
                    filelocation='/csv_file/' + renamefile
                    df.to_csv(csvfile, encoding="ISO-8859-1", index=False)
                    File.objects.create(name=name, description=description,filelocation=filelocation, user=userinstance)

                else:#Upload via File
                    file = request.FILES['filedir']
                    df = pd.read_csv(file, encoding="ISO-8859-1")
                    filelocation = '/csv_file/' + renamefile
                    csvfile = settings.MEDIA_ROOT + '/csv_file/' + renamefile
                    df.to_csv(csvfile, encoding="ISO-8859-1", index=False)
                    File.objects.create(name=name, description=description, filelocation=filelocation, user=userinstance)

                return HttpResponseRedirect(reverse('datalist'))

            except:
                messages.error(request, "File must be in CSV format.")


    return render(request, 'uploadcsv/uploadcsv.html')