from django import forms

from companies.models import Company

from .models import RATING_CHOICES, Review


class ContactForm(forms.Form):
    name = forms.CharField(label="Ime: ", max_length=255)
    email = forms.EmailField(label="Email: ")
    subject = forms.CharField(label="Naslov: ", max_length=100)
    message = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "8"}), label="Poruka: "
    )


class ReviewForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        label="Kompanija: ",
        empty_label="Izaberite kompaniju",
        queryset=Company.objects.all(),
    )
    rating = forms.ChoiceField(
        label="Ocena: ", choices=RATING_CHOICES, initial=RATING_CHOICES[4]
    )
    title = forms.CharField(label="Naslov: ")
    body = forms.CharField(
        label="Vaša recenzija: ",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "cols": 30,
                "rows": 5,
                "maxlength": "500",
            }
        ),
    )

    class Meta:
        model = Review
        fields = ["company", "rating", "title", "body"]
