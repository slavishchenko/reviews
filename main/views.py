import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.html import escape
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import FormView

from companies.models import Company

from .forms import ContactForm, ReviewForm
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


class ContactView(FormView):
    template_name = "main/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("contact_done")

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def form_valid(self, form):
        title = form.cleaned_data["subject"]
        name = form.cleaned_data["name"]
        subject = f"/ [Kontakt]: {title} - {name}"
        message = render_to_string(
            "main/contact_email_template.html",
            {
                "title": title,
                "body": form.cleaned_data["message"],
                "name": name,
                "email": form.cleaned_data["email"],
                "protocol": "https" if self.request.is_secure() else "http",
            },
        )
        mail_admins(subject=subject, message=message)
        return super().form_valid(form)


class ContactDoneView(TemplateView):
    template_name = "main/contact_done.html"


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
        body = json.loads(request.body)
        review_id = body.get("review_id")
        review = get_object_or_404(Review, id=review_id)
        if request.user not in review.likes.all():
            review.likes.add(request.user)
            review.like_count += 1
            review.save()
            like_count = review.like_count
        else:
            review.likes.remove(request.user)
            review.like_count -= 1
            review.save()
            like_count = review.like_count
        return JsonResponse({"like_count": like_count})
    else:
        return HttpResponse("418. I'm a teapot", status=418)


class BaseUserInteractionView(LoginRequiredMixin, View):
    object = None
    liked = False
    disliked = False

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        body = json.loads(self.request.body)
        id = body.get("review_id")
        return get_object_or_404(Review, id=id)

    def get_like_count(self):
        return self.object.like_count

    def get(self, request, *args, **kwargs):
        return HttpResponse("418. I'm a teapot", status=418)


class LikeView(BaseUserInteractionView):
    def post(self, request, *args, **kwargs):
        if request.user not in self.object.likes.all():
            if request.user not in self.object.dislikes.all():
                self.object.likes.add(request.user)
                self.object.like_count += 1
                self.object.save()
                self.liked = True
            else:
                self.disliked = True
                self.object.dislikes.remove(request.user)
                self.object.likes.add(request.user)
                self.object.like_count += 2
                self.liked = True
                self.object.save()
        else:
            self.object.likes.remove(request.user)
            self.object.like_count -= 1
            self.object.save()
            self.liked = False

        return JsonResponse(
            {
                "like_count": self.get_like_count(),
                "liked": self.liked,
                "disliked": self.disliked,
            }
        )


class DislikeView(BaseUserInteractionView):
    def post(self, request, *args, **kwargs):
        if request.user not in self.object.dislikes.all():
            if request.user not in self.object.likes.all():
                self.object.dislikes.add(request.user)
                self.object.like_count -= 1
                self.object.save()
                self.disliked = True
            else:
                self.liked = True
                self.object.likes.remove(request.user)
                self.object.dislikes.add(request.user)
                self.object.like_count -= 2
                self.disliked = True
                self.object.save()
        else:
            self.object.dislikes.remove(request.user)
            self.object.like_count += 1
            self.object.save()
            self.disliked = False

        return JsonResponse(
            {
                "like_count": self.get_like_count(),
                "disliked": self.disliked,
                "liked": self.liked,
            }
        )
