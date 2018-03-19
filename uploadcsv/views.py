from django.shortcuts import render, get_object_or_404
from .models import File, UploadForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
import pandas as pd
import io



def viewcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'viewcsv.html', {'file': file})

def opencsv(request, pk):
    filelocation = str(get_object_or_404(File, pk=pk).filelocation)
    csvfile=settings.MEDIA_ROOT + '/' + filelocation
    data = pd.read_csv(csvfile, encoding = "ISO-8859-1")
    pd.set_option('display.max_colwidth', -1)

    if 'dropna' in request.POST:
        data = data.dropna(how='all')
        data.to_csv(csvfile, encoding="ISO-8859-1", index=False)
    elif 'strip' in request.POST:
        index = request.POST['index']
        data[index]=data[index].str.strip()
        data.to_csv(csvfile, encoding="ISO-8859-1",index=False)


    def process_content_info(content: pd.DataFrame):
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
    context = {'loaded_data': data_html, 'data_info':data_info, 'pk':pk}
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

