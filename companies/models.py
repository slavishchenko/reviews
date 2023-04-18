import statistics
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"


class PaymentOption(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Address(models.Model):
    street_name = models.CharField(max_length=100)
    street_number = models.CharField(max_length=25)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.IntegerField()

    def __str__(self):
        return f"{self.street_name} {self.street_number}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "addresses"


class Company(models.Model):
    name = models.CharField(max_length=150)
    website_url = models.CharField(max_length=150)
    description = models.TextField(max_length=255, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="shops")
    payment_options = models.ManyToManyField(
        PaymentOption, related_name="shops", blank=True
    )
    delivery_time = models.CharField(max_length=50, blank=True, null=True)
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        related_name="companies",
        blank=True,
        null=True,
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    social_media_link = models.URLField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    slug = models.SlugField(editable=False)

    @property
    def domain_name(self):
        return urlparse(self.website_url).netloc

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

    class Meta:
        verbose_name_plural = "Companies"
