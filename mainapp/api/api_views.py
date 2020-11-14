from typing import List

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from ..models import Category, Smartphone
from .serializers import CategorySerializer, SmartphoneSerializer


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SmartphoneListAPIView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']
