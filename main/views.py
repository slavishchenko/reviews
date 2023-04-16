from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView

from .forms import ReviewForm


# Create your views here.
def index(request):
    return render(request, "main/index.html")


class ReviewFormView(FormView):
    template_name = "main/review_create_form.html"
    form_class = ReviewForm
    success_url = reverse_lazy("index")

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
        messages.success(self.request, f"Vaša recenzija je sačuvana.")
        return super().form_valid(form)
