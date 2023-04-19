from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

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
    success_url = reverse_lazy("company_create_done")
    form_class = CompanyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context

    def form_valid(self, form):
        company = form.save(commit=False)
        company.submitted_by = self.request.user
        company.approved = True
        company.save()
        return super().form_valid(form)


class CompanyCreateDoneView(TemplateView):
    template_name = "companies/company_create_done.html"


class CompanyListView(ListView):
    model = Company
    template_name = "companies/company_list.html"
    context_object_name = "company_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context
