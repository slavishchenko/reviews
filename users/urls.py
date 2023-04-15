from django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
]
