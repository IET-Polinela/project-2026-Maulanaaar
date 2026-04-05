from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='home'),
    path('add/', views.add_report, name='add_report'),
    path('reports/', views.report_list, name='report_list'),
    path('edit/<int:pk>/', views.edit_report, name='edit_report'),
    path('delete/<int:pk>/', views.delete_report, name='delete_report'),
]