from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import messages
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# CUSTOM LOGIN VIEW
class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Login berhasil! Selamat datang 👋")
        return super().form_valid(form)


urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # MAIN APP
    path('', include('main_app.urls')),

    # USER MANAGEMENT WEB
    path('user/', include('usermanagement_24782050.urls')),

    # DASHBOARD
    path('dashboard/', include('dashboard_24782050.urls')),

    # REST API REPORT
    path('api/', include('main_app.api_urls')),

    # API REGISTER CITIZEN
    path('api/auth/', include('usermanagement_24782050.api_urls')),

    # JWT TOKEN LOGIN & REFRESH
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # LOGIN WEB DJANGO
    path('login/', CustomLoginView.as_view(), name='login'),

    # LOGOUT WEB DJANGO
    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='home'),
        name='logout'
    ),
]