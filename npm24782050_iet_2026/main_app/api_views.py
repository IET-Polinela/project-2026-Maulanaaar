from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Report
from .serializers import ReportSerializer
from .permissions import IsOwnerAndDraftOnly


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def get_queryset(self):
        user = self.request.user

        # Jika user belum login, data tidak ditampilkan.
        if not user.is_authenticated:
            return Report.objects.none()

        # Lab 10:
        # List dan Detail laporan dapat diakses semua user yang sudah login.
        return Report.objects.all().order_by('-created_at')

    def get_permissions(self):
        # List, detail, dan create wajib login.
        if self.action in ['list', 'retrieve', 'create']:
            permission_classes = [permissions.IsAuthenticated]

        # Edit dan delete wajib login,
        # harus pemilik laporan dan status masih DRAFT.
        elif self.action in ['update', 'partial_update', 'destroy']:
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
        if getattr(user, 'is_admin', False):
            raise PermissionDenied("Admin tidak diperbolehkan membuat laporan sebagai Citizen.")

        if not getattr(user, 'is_member', False):
            raise PermissionDenied("Hanya Citizen yang dapat membuat laporan.")

        # Reporter otomatis dari user login JWT.
        serializer.save(reporter=user, status='DRAFT')