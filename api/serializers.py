from rest_framework import serializers

from companies.models import Company


class CompanySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Company
        fields = "__all__"
