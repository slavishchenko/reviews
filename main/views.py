import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.html import escape
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormView

from companies.models import Company

from .forms import ReviewForm
from .models import Review


class IndexView(View):
    template_name = "main/index.html"
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        company_list = (
            Company.objects.all().filter(approved=True)[:6] or Company.objects.all()
        )
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "company_list": company_list,
                "home_nav_link_class": "active",
            },
        )


class ReviewFormView(FormView):
    template_name = "main/review_create_form.html"
    form_class = ReviewForm
    success_url = reverse_lazy("review_create_done")

    def get(self, request, *args, **kwargs):
        if request.session.get("form_initial"):
            form = self.form_class(initial=request.session.get("form_initial"))
            request.session.pop("form_initial")
            return render(request, self.template_name, {"form": form})
        return render(request, self.template_name, {"form": self.form_class})

    def form_valid(self, form):
        review = form.save(commit=False)
        if not self.request.user.is_authenticated:
            self.request.session["form_initial"] = self.request.POST
            redirect_url = reverse("account_login")
            return HttpResponseRedirect(
                f"{redirect_url}?next=/recenzija/",
            )
        review.author = self.request.user
        review.save()
        return super().form_valid(form)


class ReviewCreateDone(TemplateView):
    template_name = "main/review_create_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["company"] = self.request.user.reviews.last().company
        return context


class CompanySearchView(ListView):
    template_name = "main/search.html"
    model = Company
    context_object_name = "company_list"

    def get_queryset(self):
        qs = Company.objects.all()
        q = escape(self.request.GET.get("q", ""))
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


@login_required
def like(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        review_id = json_data.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        review.likes.add(request.user)
        review.like_count += 1
        review.save()
        return JsonResponse({"result": review.like_count})
