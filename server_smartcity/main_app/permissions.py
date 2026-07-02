from rest_framework import permissions


class IsOwnerAndDraftOnly(permissions.BasePermission):
    """
    Permission untuk laporan Citizen.

    PUT, PATCH, DELETE hanya boleh jika:
    1. User adalah pemilik laporan/reporter
    2. Status laporan masih DRAFT

    Jika status sudah REPORTED, VERIFIED, IN_PROGRESS, atau RESOLVED,
    laporan menjadi read-only.
    """

    message = "Laporan hanya dapat diubah oleh pemilik saat status masih DRAFT."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            obj.reporter_id == request.user.id
            and obj.status == "DRAFT"
        )