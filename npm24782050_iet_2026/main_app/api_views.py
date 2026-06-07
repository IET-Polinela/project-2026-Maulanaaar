from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOnly


class ReportPagination(PageNumberPagination):
    # Lab 12: maksimal 10 item per halaman
    page_size = 10

    # Supaya bisa dipakai untuk bypass pagination saat menghitung summary sidebar
    # Contoh: /api/report/?tab=my_reports&page_size=1000
    page_size_query_param = "page_size"
    max_page_size = 1000


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    pagination_class = ReportPagination

    def get_queryset(self):
        user = self.request.user

        # Jika user belum login, data tidak ditampilkan.
        if not user.is_authenticated:
            return Report.objects.none()

        # Lab 12:
        # Sorting berdasarkan laporan yang terakhir diperbarui.
        queryset = Report.objects.all().order_by("-updated_at")

        # Membaca parameter tab dari URL.
        # Contoh:
        # /api/report/?tab=my_reports
        # /api/report/?tab=feed
        tab = self.request.query_params.get("tab", None)

        if tab == "my_reports":
            # Menampilkan hanya laporan milik user yang sedang login.
            queryset = queryset.filter(reporter=user)

        elif tab == "feed":
            # Menampilkan laporan warga lain yang statusnya bukan DRAFT.
            # DRAFT tidak boleh masuk Feed Kota.
            queryset = queryset.exclude(reporter=user).exclude(status="DRAFT")

        else:
            # Default jika parameter tab tidak dikirim.
            # User login dapat melihat:
            # 1. Semua laporan yang bukan DRAFT
            # 2. DRAFT miliknya sendiri
            queryset = queryset.filter(
                Q(status="DRAFT", reporter=user) | ~Q(status="DRAFT")
            )

        return queryset

    def get_permissions(self):
        # List, detail, dan create wajib login.
        if self.action in ["list", "retrieve", "create"]:
            permission_classes = [permissions.IsAuthenticated]

        # Edit dan delete wajib login,
        # harus pemilik laporan dan status masih DRAFT.
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

        # Create laporan hanya untuk Citizen/member.
        if getattr(user, "is_admin", False):
            raise PermissionDenied(
                "Admin tidak diperbolehkan membuat laporan sebagai Citizen."
            )

        if not getattr(user, "is_member", False):
            raise PermissionDenied("Hanya Citizen yang dapat membuat laporan.")

        # Reporter otomatis dari user login JWT.
        # Default tetap DRAFT.
        serializer.save(reporter=user, status="DRAFT")