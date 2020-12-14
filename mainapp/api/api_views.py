from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from ..models import Category, Customer
from .serializers import CategorySerializer, CustomerSerializer


class CategoryPagination(PageNumberPagination):

    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 10


class CategoryListAPIView(ListAPIView):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all()


class CustomersListAPIView(ListAPIView):

    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
