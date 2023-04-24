from rest_framework import serializers

from companies.models import Company
from main.models import Review


class CompanySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)
    average_rating = serializers.ReadOnlyField()
    review_count = serializers.ReadOnlyField()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "website_url",
            "description",
            "category",
            "payment_options",
            "delivery_time",
            "address",
            "phone_number",
            "email_address",
            "social_media_link",
            "date_added",
            "submitted_by",
            "updated_by",
            "approved_by",
            "approved",
            "slug",
            "average_rating",
            "review_count",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
