from django.http import HttpResponse

def home(request):
    return HttpResponse('<h1>Sistem Prapemprosesan Data untuk Sokongan Eksekutif Universiti</h1>')