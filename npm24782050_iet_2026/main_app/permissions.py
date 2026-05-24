from rest_framework import permissions


class IsOwnerAndDraftOnly(permissions.BasePermission):
    """
    Permission Lab 10:
    PUT, PATCH, DELETE hanya boleh jika:
    1. User adalah pemilik laporan/reporter
    2. Status laporan masih DRAFT
    """

    def has_object_permission(self, request, view, obj):
        return obj.reporter == request.user and obj.status == 'DRAFT'