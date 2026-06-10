from django.contrib import admin
from .models import CustomUser

# 🔥 REGISTER CUSTOM USER
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_admin', 'is_member')
    list_filter = ('is_staff', 'is_superuser', 'is_admin', 'is_member')
    search_fields = ('username', 'email')