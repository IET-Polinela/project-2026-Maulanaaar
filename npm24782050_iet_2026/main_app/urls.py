from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('reports/', ReportListView.as_view(), name='report_list'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    path('reports/add/', ReportCreateView.as_view(), name='add_report'),
    path('reports/<int:pk>/edit/', ReportUpdateView.as_view(), name='edit_report'),
    path('reports/<int:pk>/delete/', ReportDeleteView.as_view(), name='delete_report'),

    # 🔥 STATUS
    path('reports/<int:pk>/status/', ReportUpdateStatusView.as_view(), name='update_status'),
]