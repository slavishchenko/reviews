import statistics

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

    @property
    def average_rating(self):
        try:
            average = round(
                statistics.mean([review.rating for review in self.reviews.all()]), 2
            )
        except statistics.StatisticsError:
            average = None
        return average

    def __str__(self) -> str:
        return self.name
