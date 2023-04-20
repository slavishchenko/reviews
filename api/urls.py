from django.urls import path

from . import views

urlpatterns = [
    path(
        "kompanije/<int:category_id>/",
        views.CompanyListView.as_view(),
        name="api_company_list",
    )
]
