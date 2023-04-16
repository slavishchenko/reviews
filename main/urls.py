from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recenzija/", views.ReviewFormView.as_view(), name="review_create"),
]
