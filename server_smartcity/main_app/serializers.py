from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
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
            'reporter_name',
            'is_owner',

            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'reporter',
            'reporter_name',
            'is_owner',
            'created_at',
            'updated_at',
        ]

    def get_reporter(self, obj):
        return "Warga Anonim"

    def get_reporter_name(self, obj):
        request = self.context.get("request")

        if not request:
            return "Warga Anonim"

        if request.query_params.get("tab") == "my_reports":
            return obj.reporter.username

        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            return obj.reporter == request.user

        return False

    def validate_status(self, value):
        allowed_status = ["DRAFT", "REPORTED"]

        if value not in allowed_status:
            raise serializers.ValidationError(
                "Status hanya boleh DRAFT atau REPORTED untuk pengguna Citizen."
            )

        return value