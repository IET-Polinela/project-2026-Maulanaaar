from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # halaman utama
    path('', include('main_app.urls')),

    # halaman about
    path('about/', include('about.urls')),

    # halaman contacts
    path('contacts/', include('contacts.urls')),
]