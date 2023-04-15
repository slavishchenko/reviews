from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recenzija/", views.add_a_review, name="add_a_review"),
]
