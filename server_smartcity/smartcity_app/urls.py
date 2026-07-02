from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import messages

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django_scalar.views import scalar_viewer


# CUSTOM LOGIN VIEW
class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Login berhasil! Selamat datang 👋")
        return super().form_valid(form)


urlpatterns = [
    # ADMIN DJANGO
    path('admin/', admin.site.urls),

    # LOGIN WEB DJANGO
    path('login/', CustomLoginView.as_view(), name='login'),

    # LOGOUT WEB DJANGO
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),

    # USER MANAGEMENT WEB
    path('user/', include('usermanagement_24782050.urls')),

    # DASHBOARD ADMIN
    path('dashboard/', include('dashboard_24782050.urls')),

    # API REGISTER CITIZEN
    path('api/auth/', include('usermanagement_24782050.api_urls')),

    # JWT TOKEN LOGIN & REFRESH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # OPENAPI SCHEMA
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # SWAGGER UI DOCUMENTATION
    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),

    # SCALAR UI DOCUMENTATION
    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),

    # REST API REPORT
    # Ini harus berada sebelum MAIN APP agar /api/report/<id>/
    # masuk ke ReportViewSet, bukan ke route lama di main_app.urls.
    path('api/', include('main_app.api_urls')),

    # MAIN APP
    # Harus diletakkan paling bawah supaya tidak menabrak route API.
    path('', include('main_app.urls')),
]