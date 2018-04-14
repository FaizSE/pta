from django.shortcuts import render, get_object_or_404
from uploadcsv.models import File
from django.conf import settings
import pandas as pd
import numpy as np
from django.contrib import messages


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

    # def process_content_info(content: pd.DataFrame):#Get df.info() in HTML
    #     content_info = io.StringIO()
    #     content.info(buf=content_info)
    #     str_ = content_info.getvalue()
    #     lines = str_.split("\n")
    #     table = io.StringIO("\n".join(lines[3:-3]))
    #     datatypes = pd.read_table(table, delim_whitespace=True, names=["column", "count", "null", "dtype"])
    #     datatypes.set_index("column", inplace=True)
    #     info = '<br/>'.join(lines[0:2] + lines[-2:-1])
    #     return info, datatypes

    def overwritedata():
        data.to_csv(csvfile, encoding="ISO-8859-1",index=False)
        colname = list(data)
        coltype = list(data.dtypes)  # Get list of headers type
        colnametype = np.column_stack((colname, coltype))  # Merge into 2D matrix
        data_html = data.to_html()
        data_html = data_html.replace("\\r", "")
        data_html = data_html.replace("\\n", "<br/>")
        context = {'loaded_data': data_html, 'pk': pk, 'colname': colname, 'colnametype': colnametype}
        return render(request, 'preprocess/opencsv.html', context)

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

    elif 'fillmean' in request.POST:#Replace missing data with mean
        coly = request.POST['coly']
        data[coly] = data[coly].fillna(data[coly].mean())
        overwritedata()

    elif 'fillmode' in request.POST:#Replace missing data with mode
        colz = request.POST['colz']
        data[colz] = data[colz].fillna(data[colz].mode()[0])
        overwritedata()

    elif 'modcol' in request.POST:#Replace character
        modchar = request.POST['modchar']
        oldchar = request.POST['oldchar']
        newchar = request.POST['newchar']

        oldchar = oldchar.replace("(", "\(")
        oldchar = oldchar.replace(")", "\)")

        data[modchar] = data[modchar].str.replace(oldchar, newchar)
        overwritedata()

    elif 'lstrip' in request.POST:#Remove left whitespace
        stripcol = request.POST['stripcol']
        data[stripcol]=data[stripcol].str.lstrip()
        overwritedata()

    elif 'rstrip' in request.POST:#Remove right whitespace
        stripcol = request.POST['stripcol']
        data[stripcol]=data[stripcol].str.rstrip()
        overwritedata()

    elif 'strip' in request.POST:#Remove left and right whitespace
        stripcol = request.POST['stripcol']
        data[stripcol]=data[stripcol].str.strip()
        overwritedata()

    elif 'dropcol' in request.POST:#Drop column
        delcol = request.POST['delcol']
        data = data.drop(columns=[delcol])
        colname = list(data)
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
        try:
            if changetypeto=='datetime64':
                data[changetypecol] = pd.to_datetime(data[changetypecol])
            else:
                data[changetypecol] = data[changetypecol].astype(changetypeto)
            coltype = list(data.dtypes)  # Get list of headers type
            colnametype = np.column_stack((colname, coltype))  # Merge into 2D matrix
            overwritedata()

        except:
            messages.error(request, "Error, string exist in the column.")

    # data_info=process_content_info(data)
    data_html=data.style.set_properties(**{'border-color': 'black', 'border': '1px solid black'}).highlight_null(null_color='yellow').render()
    context = {'loaded_data': data_html, 'pk':pk, 'colname':colname, 'colnametype':colnametype}
    return render(request, 'preprocess/opencsv.html', context)
