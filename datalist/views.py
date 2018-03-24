from uploadcsv.models import File
from django.shortcuts import render, get_object_or_404


def datalist(request):
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})

def deletedata(request,pk):
    files = get_object_or_404(File, pk=pk)
    files.delete()
    files = File.objects.all()
    return render(request, 'datalist.html', {'files': files})
