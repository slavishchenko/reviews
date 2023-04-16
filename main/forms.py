from django import forms

from companies.models import Company

from .models import RATING_CHOICES, Review


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
        widget=forms.Textarea(attrs={"class": "form-control", "cols": 30, "rows": 5}),
    )

    class Meta:
        model = Review
        fields = ["company", "rating", "title", "body"]
