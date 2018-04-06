from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import pandas as pd
import io
from django.shortcuts import redirect


def viewcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'viewcsv.html', {'file': file})

def opencsv(request, pk):
    filelocation = str(get_object_or_404(File, pk=pk).filelocation)
    csvfile=settings.MEDIA_ROOT + '/' + filelocation
    data = pd.read_csv(csvfile, encoding = "ISO-8859-1")
    colname = list(data)
    #colname = [header.replace('"', '') for header in colname]
    pd.set_option('display.max_colwidth', -1)

    def overwritedata():
        data.to_csv(csvfile, encoding="ISO-8859-1",index=False)

    if 'dropna' in request.POST:#Remove empty data
        data = data.dropna(how='all')
        overwritedata()

    elif 'strip' in request.POST:#Remove trailing whitespace
        stripcol = request.POST['stripcol']
        data[stripcol]=data[stripcol].str.strip()
        overwritedata()

    elif 'renamecol' in request.POST:#Rename column
        oldcol = request.POST['oldcol']
        newcol = request.POST['newcol']
        data=data.rename(columns={oldcol:newcol})
        colname = list(data)
        overwritedata()

    elif 'changetype' in request.POST:#Change column type
        changetypecol = request.POST['changetypecol']
        changetypeto = request.POST['changetypeto']
        data[changetypecol] = data[changetypecol].astype(changetypeto)
        overwritedata()

    def process_content_info(content: pd.DataFrame):#Get df.info() in HTML
        content_info = io.StringIO()
        content.info(buf=content_info)
        str_ = content_info.getvalue()
        lines = str_.split("\n")
        table = io.StringIO("\n".join(lines[3:-3]))
        datatypes = pd.read_table(table, delim_whitespace=True, names=["column", "count", "null", "dtype"])
        datatypes.set_index("column", inplace=True)
        info = '<br/>'.join(lines[0:2] + lines[-2:-1])
        return info, datatypes

    data_html = data.to_html()
    data_html=data_html.replace("\\r", "")
    data_html=data_html.replace("\\n", "<br/>")
    data_info=process_content_info(data)
    context = {'loaded_data': data_html, 'data_info':data_info, 'pk':pk, 'colname':colname}
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

