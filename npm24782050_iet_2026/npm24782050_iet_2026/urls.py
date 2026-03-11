from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


def home(request):
    return HttpResponse("Django berhasil dijalankan")

def welcome(request):
    return HttpResponse("Selamat Datang")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('welcome/', welcome),
]