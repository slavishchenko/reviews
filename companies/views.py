from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from django.views.generic.edit import FormView

from main.views import ReviewFormView

from .forms import AddressForm, CompanyForm
from .models import Company


# Create your views here.
class CompanyReviewFormView(ReviewFormView):
    def get(self, request, *args, **kwargs):
        company_id = self.kwargs["id"]
        company = get_object_or_404(Company, id=company_id)
        initial = {"company": company}
        form = self.form_class(initial=initial)
        form.fields["company"].disabled = True
        return render(request, self.template_name, {"form": form})


class CompanyDetailView(DetailView):
    template_name = "companies/company.html"
    model = Company
    context_object_name = "company"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.object.reviews.all()
        return context


class CompanyCreateView(FormView):
    template_name = "companies/company_create.html"
    form_class = CompanyForm
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
