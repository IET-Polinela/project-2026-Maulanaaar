from rest_framework.routers import DefaultRouter
from .api_views import ReportViewSet

router = DefaultRouter()
router.register('reports', ReportViewSet, basename='report')

urlpatterns = router.urls