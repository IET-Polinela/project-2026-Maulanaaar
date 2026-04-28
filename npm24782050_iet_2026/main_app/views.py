from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Report
from .forms import ReportForm


# 🔥 HOME
class HomeView(TemplateView):
    template_name = 'main_app/home.html'


# 🔥 LIST
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# 🔥 DETAIL
class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/report_detail.html'
    context_object_name = 'report'


# 🔥 ADMIN CHECK
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_admin', False)

    def handle_no_permission(self):
        messages.error(self.request, "❌ Akses ditolak!")
        return redirect('report_list')


# 🔥 CREATE
class ReportCreateView(AdminRequiredMixin, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "✅ Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# 🔥 UPDATE
class ReportUpdateView(AdminRequiredMixin, UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "✏️ Laporan berhasil diperbarui!")
        return super().form_valid(form)


# 🔥 DELETE
class ReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    success_url = reverse_lazy('report_list')

    def post(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Laporan berhasil dihapus!")
        return super().post(request, *args, **kwargs)


# 🔥 UPDATE STATUS (FIX FINAL)
class ReportUpdateStatusView(View):
    def post(self, request, pk):

        print("MASUK UPDATE STATUS")  # 🔥 DEBUG

        # 🔐 CEK ADMIN
        if not request.user.is_authenticated or not getattr(request.user, 'is_admin', False):
            messages.error(request, "❌ Akses ditolak!")
            return redirect('report_list')

        report = get_object_or_404(Report, pk=pk)

        # 🔥 AMBIL STATUS
        new_status = request.POST.get('status')
        print("STATUS BARU:", new_status)

        # 🔥 VALIDASI
        allowed_status = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']

        if new_status not in allowed_status:
            messages.error(request, "❌ Status tidak valid!")
            return redirect('report_list')

        # 🔥 UPDATE
        report.status = new_status
        report.save()

        messages.success(request, f"🔄 Status diubah ke {new_status}")
        return redirect('report_list')