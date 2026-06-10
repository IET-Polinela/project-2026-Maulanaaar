from django.urls import path
from .views import *

urlpatterns = [

    # 🔥 HOME
    path('', HomeView.as_view(), name='home'),

    # 🔥 REPORT LIST
    path('reports/', ReportListView.as_view(), name='report_list'),

    # =========================================
    # 🔥 API SECTION
    # =========================================

    # DETAIL (UNTUK MODAL)
    path('api/report/<int:pk>/', report_detail_api, name='report_detail_api'),

    # 🔥 LIVE SEARCH (INI YANG WAJIB DIPAKAI)
    path('api/search/', report_search_api, name='report_search_api'),

    # =========================================
    # 🔥 CRUD
    # =========================================

    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),

    path('reports/add/', ReportCreateView.as_view(), name='add_report'),

    path('reports/<int:pk>/edit/', ReportUpdateView.as_view(), name='edit_report'),

    path('reports/<int:pk>/delete/', ReportDeleteView.as_view(), name='delete_report'),

    path('reports/<int:pk>/status/', ReportUpdateStatusView.as_view(), name='update_status'),
]