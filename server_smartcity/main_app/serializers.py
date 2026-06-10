from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            'id',
            'title',
            'category',
            'description',
            'location',
            'status',
            'reporter',
            'is_owner',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'reporter',
            'is_owner',
            'created_at',
            'updated_at',
        ]

    def get_reporter(self, obj):
        # Identitas pelapor disamarkan langsung dari backend.
        # Ini penting agar nama asli tidak bocor lewat Tab Network browser.
        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get('request')

        if request and request.user and request.user.is_authenticated:
            return obj.reporter == request.user

        return False

    def validate_status(self, value):
        # Citizen hanya boleh menyimpan laporan sebagai DRAFT
        # atau mengajukan laporan menjadi REPORTED.
        allowed_status = ['DRAFT', 'REPORTED']

        if value not in allowed_status:
            raise serializers.ValidationError(
                "Status hanya boleh DRAFT atau REPORTED untuk pengguna Citizen."
            )

        return value