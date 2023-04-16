from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("recenzija/", views.ReviewFormView.as_view(), name="review_create"),
]
