from django.views.generic import TemplateView
from django.http import JsonResponse
from django.db.models import Count
from main_app.models import Report


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total'] = Report.objects.count()
        context['reported'] = Report.objects.filter(status='REPORTED').count()
        context['resolved'] = Report.objects.filter(status='RESOLVED').count()

        context['latest_reports'] = Report.objects.order_by('-id')[:5]
        context['latest_resolved'] = Report.objects.filter(status='RESOLVED').order_by('-id')[:5]

        return context


def dashboard_data(request):
    status_data = Report.objects.values('status').annotate(total=Count('id'))
    category_data = Report.objects.values('category').annotate(total=Count('id'))

    return JsonResponse({
        'status': list(status_data),
        'category': list(category_data),
    })