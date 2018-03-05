from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_tables2.tables import Table
import pandas as pd


def opencsv(request):
    data = pd.read_csv('C:/Users/Faiz/Documents/fyp/media/csv_file/2015_FTSM_PTA.csv', encoding = "ISO-8859-1")
    df_table = Table(data.to_dict(orient='list'))
    context = {'df_table': df_table}
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