from typing import List
from django.db.models import query

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from ..models import Category, Smartphone, Notebook
from .serializers import (CategorySerializer, NotebookSerializer,
                          SmartphoneSerializer)


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class SmartphoneListAPIView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']


class NotebookListAPIView(ListAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']
