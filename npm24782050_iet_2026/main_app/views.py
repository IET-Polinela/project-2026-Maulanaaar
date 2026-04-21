from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.contrib import messages
from .models import Report
from .forms import ReportForm


# 🔥 LANDING PAGE
class HomeView(TemplateView):
    template_name = 'main_app/home.html'


# 🔥 LIST LAPORAN
class ReportListView(ListView):
    model = Report
    template_name = 'main_app/report_list.html'
    context_object_name = 'reports'


# 🔥 CREATE (ADD)
class ReportCreateView(CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/add_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "✅ Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# 🔥 UPDATE (EDIT)
class ReportUpdateView(UpdateView):
    model = Report
    form_class = ReportForm
    template_name = 'main_app/edit_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "✏️ Laporan berhasil diperbarui!")
        return super().form_valid(form)


# 🔥 DELETE (INI YANG BARU KAMU BUTUH)
class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "🗑️ Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# 🔥 UPDATE STATUS
class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.status = request.POST.get('status')
        report.save()
        messages.success(request, "🔄 Status laporan berhasil diperbarui!")
        return redirect('report_list')