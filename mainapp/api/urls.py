from django.urls import path

from .api_views import CategoryListAPIView, CustomersListAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list')
]
