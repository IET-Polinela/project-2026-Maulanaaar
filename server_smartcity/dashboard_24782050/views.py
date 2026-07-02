from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

from main_app.models import Report


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'
    login_url = 'login'

    def test_func(self):
        """
        Dashboard hanya boleh diakses oleh admin/staff.
        Warga biasa tidak boleh mendapat response 200.
        """
        user = self.request.user

        return (
            user.is_authenticated
            and (
                getattr(user, 'is_admin', False)
                or getattr(user, 'is_staff', False)
            )
        )

    def handle_no_permission(self):
        """
        Jika user belum login atau bukan admin/staff,
        arahkan kembali ke halaman login.

        Ini membuat response menjadi 302, sesuai ekspektasi test AUTH-03.
        """
        return redirect('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reports = Report.objects.exclude(status='DRAFT')

        context['total'] = reports.count()
        context['reported'] = reports.filter(status='REPORTED').count()
        context['resolved'] = reports.filter(status='RESOLVED').count()

        context['verified'] = reports.filter(status='VERIFIED').count()
        context['in_progress'] = reports.filter(status='IN_PROGRESS').count()

        context['latest_reports'] = reports.order_by('-id')[:5]
        context['latest_resolved'] = reports.filter(status='RESOLVED').order_by('-id')[:5]

        return context


def dashboard_data(request):
    """
    Endpoint data dashboard untuk Chart.js.
    Hanya admin/staff yang boleh mengakses.
    """
    user = request.user

    if not user.is_authenticated or not (
        getattr(user, 'is_admin', False)
        or getattr(user, 'is_staff', False)
    ):
        return JsonResponse({'error': 'Akses ditolak'}, status=403)

    reports = Report.objects.exclude(status='DRAFT')

    status_data = reports.values('status').annotate(total=Count('id'))
    category_data = reports.values('category').annotate(total=Count('id'))

    return JsonResponse({
        'status': list(status_data),
        'category': list(category_data),
    })