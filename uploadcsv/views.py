from django.shortcuts import render

def uploadcsv(request):
    return render(request, 'uploadcsv.html')