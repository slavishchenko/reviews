from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pretraga/", views.CompanySearchView.as_view(), name="company_search"),
    path("recenzija/", views.ReviewFormView.as_view(), name="review_create"),
    path(
        "recenzija/hvala/", views.ReviewCreateDone.as_view(), name="review_create_done"
    ),
]
