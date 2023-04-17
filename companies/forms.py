from django import forms

from .models import Address, Category, Company, PaymentOption


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label="Ime kompanije: ")
    website_url = forms.CharField(
        label="Zvanični sajt: ",
        widget=forms.TextInput(attrs={"placeholder": "https://www.naprimer.com/"}),
    )
    category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(), label="Kategorije: "
    )
    description = forms.CharField(
        label="Kratak opis: ",
        widget=forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 5}),
    )
    payment_options = forms.ModelMultipleChoiceField(
        queryset=PaymentOption.objects.all(), label="Načini plaćanja: "
    )
    delivery_time = forms.CharField(
        label="Rok isporuke: ",
        widget=forms.TextInput(attrs={"placeholder": "3 - 5 radnih dana"}),
    )
    phone_number = forms.CharField(
        label="Broj telefona: ",
        widget=forms.TextInput(attrs={"placeholder": "061 1234 567"}),
    )
    email_address = forms.EmailField(
        label="E-adresa: ",
        widget=forms.TextInput(attrs={"placeholder": "naprimer@domen.com"}),
    )
    social_media_link = forms.URLField(
        label="Link društvene mreže: ",
        widget=forms.TextInput(attrs={"placeholder": "https://instagram.com/naprimer"}),
    )

    class Meta:
        model = Company
        fields = [
            "name",
            "website_url",
            "category",
            "description",
            "payment_options",
            "delivery_time",
            "phone_number",
            "email_address",
            "social_media_link",
        ]
