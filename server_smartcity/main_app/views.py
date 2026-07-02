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
# ADMIN CHECK
# =========================================
class AdminRequiredMixin(UserPassesTestMixin):
    """
    Mixin untuk membatasi halaman backend/admin web.

    User dianggap admin jika:
    - sudah login, dan
    - memiliki is_admin=True atau is_staff=True.
    """

    def test_func(self):
        user = self.request.user
        return (
            user.is_authenticated
            and (
                getattr(user, 'is_admin', False)
                or getattr(user, 'is_staff', False)
            )
        )

    def handle_no_permission(self):
        messages.error(self.request, "❌ Akses ditolak!")
        return redirect('login')


# =========================================
# LIST REPORT
# DRAFT disembunyikan dari halaman laporan backend/admin web
# =========================================
class ReportListView(AdminRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT').order_by('-created_at')


# =========================================
# DETAIL REPORT
# DRAFT tidak bisa dibuka dari halaman detail backend/admin web
# =========================================
class ReportDetailView(AdminRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')


# =========================================
# CREATE REPORT
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
# UPDATE REPORT
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
# DELETE REPORT
# DRAFT tidak bisa dihapus dari admin/backend web
# =========================================
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def get_queryset(self):
        return Report.objects.exclude(status='DRAFT')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)


# =========================================
# UPDATE STATUS REPORT
# DRAFT tidak bisa diambil/diproses admin/backend web
# =========================================
class ReportUpdateStatusView(View):
    """
    View untuk mengubah status laporan dari portal admin.

    Alur transisi:
    REPORTED    -> VERIFIED
    VERIFIED    -> IN_PROGRESS
    IN_PROGRESS -> RESOLVED
    RESOLVED    -> final/read-only
    """

    allowed_transitions = {
        'REPORTED': ['VERIFIED'],
        'VERIFIED': ['IN_PROGRESS'],
        'IN_PROGRESS': ['RESOLVED'],
        'RESOLVED': [],
    }

    def post(self, request, pk):
        user = request.user

        if not user.is_authenticated or not (
            getattr(user, 'is_admin', False)
            or getattr(user, 'is_staff', False)
        ):
            messages.error(request, "❌ Akses ditolak!")
            return redirect('login')

        report = get_object_or_404(
            Report.objects.exclude(status='DRAFT'),
            pk=pk
        )

        # Supaya cocok dengan berbagai versi form/test:
        # ada yang mengirim "status", ada juga yang mengirim "new_status".
        new_status = request.POST.get('status') or request.POST.get('new_status')

        current_status = report.status
        valid_next_statuses = self.allowed_transitions.get(current_status, [])

        if new_status not in valid_next_statuses:
            messages.error(request, "❌ Transisi status tidak valid!")
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
    user = request.user

    if not user.is_authenticated or not (
        getattr(user, 'is_admin', False)
        or getattr(user, 'is_staff', False)
    ):
        return JsonResponse({'error': 'Akses ditolak'}, status=403)

    query = request.GET.get('q', '')

    reports = Report.objects.exclude(status='DRAFT').filter(
        Q(title__icontains=query)
        | Q(location__icontains=query)
        | Q(category__icontains=query)
    ).order_by('-created_at')

    data = {
        "reports": [
            {
                "id": r.id,
                "title": r.title,
                "location": r.location,
                "status": r.status,
            }
            for r in reports
        ]
    }

    return JsonResponse(data)