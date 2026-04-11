from django.urls import path
from .views import (
    HomeView,
    ReportCreateView,
    ReportUpdateView,
    ReportDeleteView,
    ReportDetailView,
    ReportUpdateStatusView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    path('add/', ReportCreateView.as_view(), name='add_report'),
    path('edit/<int:pk>/', ReportUpdateView.as_view(), name='edit_report'),
    path('delete/<int:pk>/', ReportDeleteView.as_view(), name='delete_report'),

    path('status/<int:pk>/', ReportUpdateStatusView.as_view(), name='update_status'),
]