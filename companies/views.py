from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, TemplateView
from django.views.generic.edit import FormView, UpdateView
from django.views.generic.list import ListView

from main.views import ReviewFormView

from .forms import (
    AddressForm,
    CompanyAddDeliveryTimeForm,
    CompanyAddEmailAddressForm,
    CompanyAddPaymentOptionsForm,
    CompanyAddPhoneNumberForm,
    CompanyAddSocialMediaForm,
    CompanyForm,
    CompanyUpdateForm,
)
from .models import Address, Company


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
        context["companies_nav_link_class"] = "active"
        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):
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
        company.approved = True  # TODO
        company.save()
        return super().form_valid(form)


class CompanyCreateDoneView(TemplateView):
    template_name = "companies/company_create_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.request.user.added_companies.last()
        return context


class CompanyListView(ListView):
    model = Company
    template_name = "companies/company_list.html"
    context_object_name = "company_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context


class CompanyUpdateView(LoginRequiredMixin, FormView):
    template_name = "companies/company_update_form.html"
    form_class = CompanyUpdateForm

    def get_instance(self):
        company_id = self.kwargs["pk"]
        self.company = get_object_or_404(Company, id=company_id)
        return self.company

    def get(self, request, *args, **kwargs):
        form = self.form_class(instance=self.get_instance())
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "company": self.get_instance(),
                "companies_nav_link_class": "active",
            },
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.get_instance())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context

    def get_success_url(self):
        return reverse_lazy(
            "company_detail",
            kwargs={
                "pk": self.kwargs["pk"],
                "company_name": self.kwargs["company_name"],
            },
        )

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context["form"] = form
        context["company"] = self.get_instance()
        return self.render_to_response(context)


class CompanyAddPaymentOptionsView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/payment_options_form.html"
    form_class = CompanyAddPaymentOptionsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context


class CompanyAddDeliveryTimeView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/delivery_time_form.html"
    form_class = CompanyAddDeliveryTimeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context


class CompanyAddAddressView(FormView):
    form_class = AddressForm
    template_name = "companies/address_form.html"

    def get_company(self):
        company_id = self.kwargs["pk"]
        return get_object_or_404(Company, id=company_id)

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {
                "form": self.form_class,
                "company": self.get_company(),
                "companies_nav_link_class": "active",
            },
        )

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company_detail",
            kwargs={
                "pk": self.get_company().pk,
                "company_name": self.get_company().name,
            },
        )

    def form_valid(self, form):
        address = form.save()
        company = self.get_company()
        company.address = address
        company.save()
        return super().form_valid(form)


class CompanyAddPhoneNumber(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/phone_number_form.html"
    form_class = CompanyAddPhoneNumberForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context


class CompanyAddEmailAddress(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/email_address_form.html"
    form_class = CompanyAddEmailAddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context


class CompanyAddSocialMediaView(LoginRequiredMixin, UpdateView):
    model = Company
    template_name = "companies/social_media_form.html"
    form_class = CompanyAddSocialMediaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["companies_nav_link_class"] = "active"
        return context
