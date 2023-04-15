from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=150)
    website_url = models.CharField(max_length=150)
    description = models.TextField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="shops"
    )
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


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

    def __str__(self):
        return self.title
