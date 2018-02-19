from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')

def uploadcsv(request):
    return render(request, 'uploadcsv.html')