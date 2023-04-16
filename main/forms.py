from django import forms

from .models import RATING_CHOICES, Company, Review


class ReviewForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        label="Kompanija: ", empty_label=None, queryset=Company.objects.all()
    )
    rating = forms.ChoiceField(
        label="Ocena: ", choices=RATING_CHOICES, initial=RATING_CHOICES[4]
    )
    title = forms.CharField(label="Naslov: ")
    body = forms.CharField(
        label="Vaša recenzija: ",
        widget=forms.Textarea(
            attrs={"class": "form-control txt-format", "cols": 30, "rows": 5}
        ),
    )

    class Meta:
        model = Review
        fields = ["company", "rating", "title", "body"]
