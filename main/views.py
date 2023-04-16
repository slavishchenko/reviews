from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView

from .forms import ReviewForm


# Create your views here.
def index(request):
    return render(request, "main/index.html")


# @method_decorator(login_required, name="dispatch")
class ReviewFormView(FormView):
    template_name = "main/review_create_form.html"
    form_class = ReviewForm
    success_url = "index"

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author = self.request.user
        review.save()
        messages.success(self.request, f"Vaša recenzija je sačuvana.")
        return super().form_valid(form)
