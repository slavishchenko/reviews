import statistics
from urllib.parse import urlparse

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
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
    zip_code = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.street_name} {self.street_number}, {self.city}, {self.country}"

    class Meta:
        verbose_name_plural = "addresses"


class Company(models.Model):
    name = models.CharField(max_length=150, unique=True)
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
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="added_companies"
    )
    updated_by = models.ManyToManyField(User, related_name="updated", blank=True)
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="approved", blank=True, null=True
    )
    approved = models.BooleanField(default=False)

    slug = models.SlugField(editable=False)

    def get_absolute_url(self):
        return reverse(
            "company_detail", kwargs={"pk": self.pk, "company_name": self.slug}
        )

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
        ordering = ["-date_added"]


class WrongCompanyInfoReprot(models.Model):
    title = models.CharField(max_length=80)
    body = models.TextField(max_length=500)
    reported_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reports"
    )
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - by {self.reported_by}"


class PendingChanges(models.Model):
    STATUS_CHOICES = (("p", "Pending"), ("a", "Approved"))

    field_name = models.CharField(max_length=150)
    new_value = models.CharField(max_length=300)
    object_id = models.PositiveIntegerField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    approved = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    submitted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="edits"
    )

    def __str__(self):
        return f"{self.field_name} / {self.new_value} / {self.object_id}"

    def save(self, *args, **kwargs):
        if self.approved:
            company = get_object_or_404(Company, id=self.object_id)
            setattr(company, self.field_name, self.new_value)
            company.save()
            self.status = "a"
        super(PendingChanges, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Pending Changes"
