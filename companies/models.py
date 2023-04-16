import statistics

from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


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
    slug = models.SlugField(editable=False)

    @property
    def average_rating(self):
        try:
            average = round(
                statistics.mean([review.rating for review in self.reviews.all()]), 1
            )
        except statistics.StatisticsError:
            average = None
        return average

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(unidecode(self.name))
        super(Company, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
