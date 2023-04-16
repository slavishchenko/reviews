from django.contrib.auth.models import User
from django.db import models

from companies.models import Company

# Create your models here.
RATING_CHOICES = (
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
)


class Review(models.Model):
    rating = models.SmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=150)
    body = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="reviews"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def rating_style(self):
        match self.rating:
            case 1:
                return "danger"
            case 2:
                return "warning"
            case 3:
                return "info"
            case _:
                return "success"

    def __str__(self):
        return self.title
