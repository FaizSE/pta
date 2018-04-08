from django.shortcuts import render, get_object_or_404
from uploadcsv.models import File
from django.conf import settings
import pandas as pd
import io
import numpy as np

def viewcsv(request, pk):
    file = get_object_or_404(File, pk=pk)
    return render(request, 'preprocess/viewcsv.html', {'file': file})

def preprocesscsv(request, pk):
    filelocation = str(get_object_or_404(File, pk=pk).filelocation)
    csvfile=settings.MEDIA_ROOT + '/' + filelocation
    data = pd.read_csv(csvfile, encoding = "ISO-8859-1")
    data = data.rename(columns=lambda x: x.strip())#Remove trailing whitespace from headers
    colname = list(data)#Get list of headers
    coltype = list(data.dtypes)#Get list of headers type
    colnametype=np.column_stack((colname, coltype))#Merge into 2D matrix
    pd.set_option('display.max_colwidth', -1)

    def overwritedata():
        data.to_csv(csvfile, encoding="ISO-8859-1",index=False)

    if 'dropna' in request.POST:#Remove empty row
        data = data.dropna(how='all')
        overwritedata()

    elif 'dropnathresh' in request.POST:#Remove row with threshold
        number = request.POST['thresh']
        number = int(number)
        data = data.dropna(thresh=number)
        overwritedata()

    elif 'dropnacol' in request.POST:#Remove row with subset
        colx = request.POST['colx']
        data = data.dropna(subset=[colx])
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

        if changetypeto=='datetime64':
            data[changetypecol] = pd.to_datetime(data[changetypecol])
        else:
            data[changetypecol] = data[changetypecol].astype(changetypeto)
        coltype = list(data.dtypes)  # Get list of headers type
        colnametype = np.column_stack((colname, coltype))  # Merge into 2D matrix
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
    context = {'loaded_data': data_html, 'data_info':data_info, 'pk':pk, 'colname':colname, 'colnametype':colnametype}
    return render(request, 'preprocess/opencsv.html', context)
