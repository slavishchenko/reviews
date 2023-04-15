from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ReviewForm


# Create your views here.
def index(request):
    return render(request, "main/index.html")


def add_a_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.save()
            messages.success(request, f"Vaša recenzija je sačuvana.")
            return redirect("index")
    form = ReviewForm()

    context = {"title": f"Podelite vaše iskustvo", "form": form}
    return render(request, "main/add_a_review.html", context)
