import importlib

from allauth.account import views as auth_views
from allauth.socialaccount import providers
from django.urls import include, path, re_path

providers_urlpatterns = []

for provider in providers.registry.get_list():
    prov_mod = importlib.import_module(provider.get_package() + ".urls")
    providers_urlpatterns += getattr(prov_mod, "urlpatterns", [])

urlpatterns = [
    path("", include(providers_urlpatterns)),
    path("signup/", auth_views.SignupView.as_view(), name="account_signup"),
    path("login/", auth_views.LoginView.as_view(), name="account_login"),
    path("logout/", auth_views.LogoutView.as_view(), name="account_logout"),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(),
        name="account_change_password",
    ),
    path(
        "password/set/",
        auth_views.PasswordSetView.as_view(),
        name="account_set_password",
    ),
    # E-mail
    path(
        "confirm-email/",
        auth_views.EmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        auth_views.ConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    # password reset
    path(
        "password/reset/",
        auth_views.PasswordResetView.as_view(),
        name="account_reset_password",
    ),
    path(
        "password/reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="account_reset_password_done",
    ),
    re_path(
        r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        auth_views.PasswordResetFromKeyView.as_view(),
        name="account_reset_password_from_key",
    ),
    path(
        "password/reset/key/done/",
        auth_views.PasswordResetFromKeyDoneView.as_view(),
        name="account_reset_password_from_key_done",
    ),
]
