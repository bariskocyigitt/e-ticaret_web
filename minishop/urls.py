from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shop.views import home, about, orders_view, signup_view

urlpatterns = [
    path("admin/", admin.site.urls),

    # İlk ekranı home yapıyoruz; home girişsiz kullanıcıyı signup'a yönlendirir
    path("", home, name="home"),

    # Auth
    path("accounts/signup/", signup_view, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Sayfalar
    path("about/", about, name="about"),
    path("orders/", orders_view, name="orders"),

    # Shop
    path("shop/", include("shop.urls")),
]
