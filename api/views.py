from rest_framework import generics, renderers

from companies.models import Company
from main.models import Review

from .serializers import CompanySerializer, ReviewSerializer


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    renderer_classes = [renderers.JSONRenderer]

    def get_queryset(self):
        queryset = Company.objects.all().filter(approved=True)
        category_id = self.request.query_params.get("category")
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        return queryset


class ReviewDetailView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
