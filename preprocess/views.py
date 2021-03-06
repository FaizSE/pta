from django.shortcuts import render, get_object_or_404
from uploadcsv.models import File
from django.conf import settings
import pandas as pd
import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')

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
        colname = list(data)
        coltype = list(data.dtypes)  # Get list of headers type
        colnametype = np.column_stack((colname, coltype))  # Merge into 2D matrix
        messages.error(request, "Succesful.")

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
        oldchar = oldchar.replace("[", "\[")
        oldchar = oldchar.replace("]", "\]")
        oldchar = oldchar.replace("-", "\-")

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

    elif 'dropduplicate' in request.POST:#Drop duplicate data
        data = data.drop_duplicates()
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
            messages.error(request, "String exist in the column.")

    data_html=data.style.set_table_attributes('class="data_html"').set_properties(**{'border':'1px solid black', 'id':'myTable'}).highlight_null(null_color='yellow').render()
    datadescribe_html=data.describe(include='all').to_html(classes=["table-striped", "table-hover"])
    context = {'loaded_data': data_html, 'pk':pk, 'colname':colname, 'colnametype':colnametype, 'datadescribe_html': datadescribe_html}
    return render(request, 'preprocess/preprocesscsv.html', context)