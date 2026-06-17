from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from drf_spectacular.utils import extend_schema

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOnly


class ReportPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Report.objects.none()

        queryset = Report.objects.all().order_by("-updated_at")

        tab = self.request.query_params.get("tab", None)

        if tab == "my_reports":
            queryset = queryset.filter(reporter=user)

        elif tab == "feed":
            # Feed Kota publik: tampilkan semua laporan selain DRAFT
            queryset = queryset.exclude(status="DRAFT")

        else:
            # Default: tampilkan laporan publik non-DRAFT + DRAFT milik sendiri
            queryset = queryset.filter(
                Q(status="DRAFT", reporter=user) | ~Q(status="DRAFT")
            )

        return queryset

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            permission_classes = [permissions.IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraftOnly
            ]

        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user

        if getattr(user, "is_admin", False):
            raise PermissionDenied(
                "Admin tidak diperbolehkan membuat laporan sebagai Citizen."
            )

        if not getattr(user, "is_member", False):
            raise PermissionDenied("Hanya Citizen yang dapat membuat laporan.")

        serializer.save(reporter=user, status="DRAFT")

    # SKENARIO 1 LAB 14:
    # Endpoint DELETE disembunyikan dari dokumentasi OpenAPI/Scalar,
    # tetapi endpoint tetap harus diamankan dengan permission DRF.
    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)