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

        # Untuk list endpoint: /api/report/
        if self.action == "list":
            tab = self.request.query_params.get("tab")

            if tab == "my_reports":
                # Tab laporan saya: tampilkan semua laporan milik user, termasuk DRAFT
                return queryset.filter(reporter=user)

            if tab == "feed":
                # Feed publik: hanya tampilkan laporan yang sudah diajukan
                return queryset.exclude(status="DRAFT")

            # Default list: DRAFT milik sendiri + laporan publik non-DRAFT
            return queryset.filter(
                Q(status="DRAFT", reporter=user) | ~Q(status="DRAFT")
            )

        # Untuk retrieve/update/delete:
        # - DRAFT milik sendiri boleh ditemukan
        # - DRAFT milik orang lain disembunyikan menjadi 404
        # - Laporan non-DRAFT boleh ditemukan, tapi update-nya dikontrol permission
        return queryset.filter(
            Q(status="DRAFT", reporter=user) | ~Q(status="DRAFT")
        )

    def get_permissions(self):
        if self.action in ["list", "retrieve", "create"]:
            permission_classes = [permissions.IsAuthenticated]

        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerAndDraftOnly,
            ]

        else:
            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user

        # Admin tidak boleh membuat laporan sebagai Citizen
        if getattr(user, "is_admin", False) or getattr(user, "is_staff", False):
            raise PermissionDenied(
                "Admin tidak diperbolehkan membuat laporan sebagai Citizen."
            )

        serializer.save(reporter=user, status="DRAFT")

    def perform_update(self, serializer):
        instance = self.get_object()
        requested_status = self.request.data.get("status", instance.status)

        # Kalau masih DRAFT, pemilik boleh simpan sebagai DRAFT atau ajukan ke REPORTED
        if instance.status == "DRAFT":
            serializer.save(status=requested_status)
            return

        # Sebenarnya bagian ini tidak akan tercapai untuk warga,
        # karena permission sudah menolak update non-DRAFT dengan 403.
        serializer.save()

    @extend_schema(exclude=True)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)