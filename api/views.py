from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from companies.models import Company

from .serializers import CompanySerializer


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Company.objects.all().filter(approved=True)
        category_id = self.kwargs.get("category_id")
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset
