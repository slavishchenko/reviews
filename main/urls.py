from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pretraga/", views.CompanySearchView.as_view(), name="company_search"),
    path("recenzija/", views.ReviewFormView.as_view(), name="review_create"),
    path(
        "recenzija/hvala/", views.ReviewCreateDone.as_view(), name="review_create_done"
    ),
    path("like/", views.LikeView.as_view(), name="like"),
    path("dislike/", views.DislikeView.as_view(), name="dislike"),
    path("kontakt/", views.ContactView.as_view(), name="contact"),
    path("kontakt/hvala/", views.ContactDoneView.as_view(), name="contact_done"),
    path("o-nama/", views.AboutUsView.as_view(), name="about_us"),
]
