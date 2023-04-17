from django.urls import path

from . import views

urlpatterns = [
    path("", views.CompanyCreateView.as_view(), name="company_create"),
    path(
        "<int:id>/recenzija/",
        views.CompanyReviewFormView.as_view(),
        name="company_review_create",
    ),
    path(
        "<int:pk>/<str:company_name>/",
        views.CompanyDetailView.as_view(),
        name="company_detail",
    ),
]
