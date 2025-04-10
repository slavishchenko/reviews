from django import forms

from .models import Address, Category, Company, PaymentOption, WrongCompanyInfoReport


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["street_name", "street_number", "city", "country"]
        labels = {
            "street_name": "Ulica: ",
            "street_number": "Broj: ",
            "city": "Grad: ",
            "country": "Država: ",
        }


class CompanyForm(forms.ModelForm):
    name = forms.CharField(label="Ime kompanije: ")
    website_url = forms.CharField(
        label="Zvanični sajt: ",
        widget=forms.TextInput(attrs={"placeholder": "https://www.naprimer.com/"}),
    )
    category = forms.ModelMultipleChoiceField(
        help_text="Držite 'Ctrl' da selektujete više opcija.",
        queryset=Category.objects.all(),
        label="Kategorije: ",
    )
    description = forms.CharField(
        label="Kratak opis: ",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "cols": 20, "rows": 5}),
    )
    payment_options = forms.ModelMultipleChoiceField(
        help_text="Držite 'Ctrl' da selektujete više opcija.",
        required=False,
        queryset=PaymentOption.objects.all(),
        label="Načini plaćanja: ",
    )
    delivery_time = forms.CharField(
        required=False,
        label="Rok isporuke: ",
        widget=forms.TextInput(attrs={"placeholder": "3 - 5 radnih dana"}),
    )
    phone_number = forms.CharField(
        required=False,
        label="Broj telefona: ",
        widget=forms.TextInput(attrs={"placeholder": "011 1-123-123"}),
    )
    email_address = forms.EmailField(
        required=False,
        label="E-adresa: ",
        widget=forms.TextInput(attrs={"placeholder": "naprimer@domen.com"}),
    )
    social_media_link = forms.URLField(
        required=False,
        label="Link društvene mreže: ",
        widget=forms.TextInput(attrs={"placeholder": "https://instagram.com/naprimer"}),
    )

    class Meta:
        model = Company
        fields = [
            "name",
            "category",
            "website_url",
            "description",
            "payment_options",
            "delivery_time",
            "phone_number",
            "email_address",
            "social_media_link",
        ]


class CompanyUpdateForm(CompanyForm):
    pass


class CompanyAddPaymentOptionsForm(forms.ModelForm):
    payment_options = forms.ModelMultipleChoiceField(
        help_text="Držite 'Ctrl' da selektujete više opcija.",
        queryset=PaymentOption.objects.all(),
        label="Načini plaćanja: ",
    )

    class Meta:
        model = Company
        fields = ["payment_options"]


class CompanyAddDeliveryTimeForm(forms.ModelForm):
    delivery_time = forms.CharField(
        label="Rok isporuke: ",
        widget=forms.TextInput(attrs={"placeholder": "3 - 5 radnih dana"}),
    )

    class Meta:
        model = Company
        fields = ["delivery_time"]


class CompanyAddPhoneNumberForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["phone_number"]
        labels = {"phone_number": "Broj telefona: "}


class CompanyAddEmailAddressForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["email_address"]
        labels = {"email_address": "E-adresa: "}
        widgets = {
            "email_address": forms.TextInput(
                attrs={"placeholder": "naprimer@domen.com"}
            )
        }


class CompanyAddSocialMediaForm(forms.ModelForm):
    social_media_link = forms.URLField(
        label="Link društvene mreže: ",
        widget=forms.TextInput(attrs={"placeholder": "https://instagram.com/naprimer"}),
    )

    class Meta:
        model = Company
        fields = ["social_media_link"]


class WrongCompanyInfoReportForm(forms.ModelForm):
    class Meta:
        model = WrongCompanyInfoReport
        fields = ["title", "body"]
        labels = {"title": "Naslov: ", "body": "Poruka: "}
