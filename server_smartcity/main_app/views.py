from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
)
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse
from django.db.models import Q

from .models import Report
from .forms import ReportForm


# =========================================
# HOME
# =========================================
class HomeView(TemplateView):
    template_name = 'main_app/home.html'


# =========================================
# LIST REPORT
# DRAFT disembunyikan dari halaman laporan backend/admin web
# =========================================
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT').order_by('-created_at')


# =========================================
# DETAIL REPORT
# DRAFT tidak bisa dibuka dari halaman detail backend/admin web
# =========================================
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')


# =========================================
# ADMIN CHECK
# =========================================
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_admin', False)

    def handle_no_permission(self):
        messages.error(self.request, "❌ Akses ditolak!")
        return redirect('report_list')


# =========================================
# CREATE
# =========================================
class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "✅ Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# =========================================
# UPDATE
# DRAFT tidak bisa diedit oleh admin/backend web
# =========================================
class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')

    def form_valid(self, form):
        messages.success(self.request, "✏️ Laporan berhasil diperbarui!")
        return super().form_valid(form)


# =========================================
# DELETE
# DRAFT tidak bisa dihapus dari admin/backend web
# =========================================
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)


# =========================================
# UPDATE STATUS
# DRAFT tidak bisa diambil/diproses admin/backend web
# =========================================
class ReportUpdateStatusView(View):
    def post(self, request, pk):

        if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
            messages.error(request, "❌ Akses ditolak!")
            return redirect('report_list')

        report = get_object_or_404(
            Report.objects.exclude(status='DRAFT'),
            pk=pk
        )

        new_status = request.POST.get('status')

        allowed_status = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']

        if new_status not in allowed_status:
            messages.error(request, "❌ Status tidak valid!")
            return redirect('report_list')

        report.status = new_status
        report.save()

        messages.success(request, f"🔄 Status diubah ke {new_status}")
        return redirect('report_list')


# =========================================
# API DETAIL UNTUK MODAL
# DRAFT tidak dikembalikan
# =========================================
def report_detail_api(request, pk):
    report = get_object_or_404(
        Report.objects.exclude(status='DRAFT'),
        pk=pk
    )

    data = {
        'title': report.title,
        'category': report.category,
        'description': report.description,
        'location': report.location,
        'status': report.status,
    }

    return JsonResponse(data)


# =========================================
# LIVE SEARCH API
# DRAFT disembunyikan dari hasil pencarian
# =========================================
def report_search_api(request):
    query = request.GET.get('q', '')

    reports = Report.objects.exclude(status='DRAFT').filter(
        Q(title__icontains=query) |
        Q(location__icontains=query) |
        Q(category__icontains=query)
    ).order_by('-created_at')

    data = {
        "reports": [
            {
                "id": r.id,
                "title": r.title,
                "location": r.location,
                "status": r.status
            }
            for r in reports
        ]
    }

    return JsonResponse(data)