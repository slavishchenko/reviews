from django.urls import path

from . import views

urlpatterns = [
    path(
        "kompanije/",
        views.CompanyListView.as_view(),
        name="api_company_list",
    ),
    path(
        "recenzija/<int:pk>/",
        views.ReviewDetailView.as_view(),
        name="api_review_detail",
    ),
]
