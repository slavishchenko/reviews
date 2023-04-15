from allauth.account import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("google/login/", views.google_login, name="account_google_login"),
    path("logout/", auth_views.LogoutView.as_view()),
]
