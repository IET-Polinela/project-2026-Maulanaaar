from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import messages


# 🔥 CUSTOM LOGIN VIEW (BIAR ADA ALERT SUKSES)
class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        messages.success(self.request, "✅ Login berhasil! Selamat datang 👋")
        return super().form_valid(form)


urlpatterns = [
    # 🔥 ADMIN
    path('admin/', admin.site.urls),

    # 🔥 MAIN APP
    path('', include('main_app.urls')),

    # 🔥 USER MANAGEMENT
    path('user/', include('usermanagement_24782050.urls')),

    # 🔥 LOGIN (SUDAH CUSTOM)
    path('login/', CustomLoginView.as_view(), name='login'),

    # 🔥 LOGOUT
    path('logout/', auth_views.LogoutView.as_view(
        next_page='home'
    ), name='logout'),
]