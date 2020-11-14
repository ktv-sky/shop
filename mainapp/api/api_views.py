from django.db.models import query
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from ..models import Category, Notebook, Smartphone, Customer
from .serializers import (CategorySerializer, NotebookSerializer,
                          SmartphoneSerializer, CustomerSerializer)


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


class SmartphoneDetailAPIView(RetrieveAPIView):

    serializer_class = SmartphoneSerializer
    queryset = Smartphone.objects.all()
    lookup_field = 'id'


class NotebookDetailAPIView(RetrieveAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    lookup_field = 'id'


class CustomersListAPIView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
