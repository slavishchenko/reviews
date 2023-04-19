from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.CompanyListView.as_view(), name="company_list"),  # Change!
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
        "<int:pk>/<str:company_name>/broj-telefona/",
        views.CompanyUpdatePhoneNumber.as_view(),
        name="company_update_phone_number",
    ),
    path(
        "<int:pk>/<str:company_name>/e-adresa/",
        views.CompanyUpdatePhoneNumber.as_view(),
        name="company_update_email_address",
    ),
    path(
        "<int:pk>/<str:company_name>/",
        views.CompanyDetailView.as_view(),
        name="company_detail",
    ),
]
