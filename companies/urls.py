from django.urls import path

from . import views

urlpatterns = [
    path("dodaj/", views.CompanyCreateView.as_view(), name="company_create"),
    path("hvala/", views.CompanyCreateDoneView.as_view(), name="company_create_done"),
    path(
        "<int:id>/recenzija/",
        views.CompanyReviewFormView.as_view(),
        name="company_review_create",
    ),
    path(
        "<int:pk>/<str:company_name>/izmeni/",
        views.CompanyUpdateView.as_view(),
        name="company_update",
    ),
    path(
        "<int:pk>/<str:company_name>/načini-plaćanja/dodaj",
        views.CompanyAddPaymentOptionsView.as_view(),
        name="company_add_payment_options",
    ),
    path(
        "<int:pk>/<str:company_name>/rok-isporuke/dodaj",
        views.CompanyAddDeliveryTimeView.as_view(),
        name="company_add_delivery_time",
    ),
    path(
        "<int:pk>/<str:company_name>/adresa/dodaj/",
        views.CompanyAddAddressView.as_view(),
        name="company_add_address",
    ),
    path(
        "<int:pk>/<str:company_name>/broj-telefona/dodaj/",
        views.CompanyAddPhoneNumber.as_view(),
        name="company_add_phone_number",
    ),
    path(
        "<int:pk>/<str:company_name>/e-adresa/dodaj/",
        views.CompanyAddEmailAddress.as_view(),
        name="company_add_email_address",
    ),
    path(
        "<int:pk>/<str:company_name>/društvena-mreža/dodaj/",
        views.CompanyAddSocialMediaView.as_view(),
        name="company_add_social_media",
    ),
    path(
        "<int:pk>/<str:company_name>/",
        views.CompanyDetailView.as_view(),
        name="company_detail",
    ),
    path(
        "<int:pk>/<str:company_name>/prijavi/",
        views.ReportWrongCompanyInfoView.as_view(),
        name="company_report_wrong_info",
    ),
    path(
        "prijavi/hvala/",
        views.ReportWrongInfoDoneView.as_view(),
        name="company_report_wrong_info_done",
    ),
]
