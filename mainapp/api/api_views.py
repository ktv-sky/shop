from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from ..models import Category, Customer, Notebook, Smartphone
from .serializers import (CategorySerializer, CustomerSerializer,
                          NotebookSerializer, SmartphoneSerializer)


class CategoryPagination(PageNumberPagination):

    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 10


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
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
