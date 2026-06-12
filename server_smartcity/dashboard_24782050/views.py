from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from main_app.models import Report


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reports = Report.objects.exclude(status='DRAFT')

        context['total'] = reports.count()
        context['reported'] = reports.filter(status='REPORTED').count()
        context['resolved'] = reports.filter(status='RESOLVED').count()

        context['latest_reports'] = reports.order_by('-id')[:5]
        context['latest_resolved'] = reports.filter(status='RESOLVED').order_by('-id')[:5]

        return context


def dashboard_data(request):
    reports = Report.objects.exclude(status='DRAFT')

    status_data = reports.values('status').annotate(total=Count('id'))
    category_data = reports.values('category').annotate(total=Count('id'))

    return JsonResponse({
        'status': list(status_data),
        'category': list(category_data),
    })