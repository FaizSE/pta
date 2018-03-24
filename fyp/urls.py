"""fyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from homepage import views
from accounts import views as accounts_views
from datalist import views as datalist_views
from uploadcsv import views as uploadcsv_views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^opencsv/(?P<pk>\d+)/$', uploadcsv_views.opencsv, name='opencsv'),
    url(r'^uploadcsv/new/$', uploadcsv_views.newcsv, name='newcsv'),
    url(r'^datalist/view/(?P<pk>\d+)/$', uploadcsv_views.viewcsv, name='viewcsv'),
    url(r'^datalist/delete/(?P<pk>\d+)/$', datalist_views.deletedata, name='deletedata'),
    url(r'^datalist', datalist_views.datalist, name='datalist'),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
