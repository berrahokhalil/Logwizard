from django.urls import path

from . import views

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile_view, name="profile"),
    path("log_files/", views.log_files_view, name="log_files_view"),
    path("errors/", views.errors_view, name="errors_view"),
    path("about/", views.about_view, name="about_view"),
]