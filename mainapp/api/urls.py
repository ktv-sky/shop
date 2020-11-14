from django.urls import path

from .api_views import (CategoryListAPIView, CustomersListAPIView,
                        NotebookDetailAPIView, NotebookListAPIView,
                        SmartphoneDetailAPIView, SmartphoneListAPIView)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('smartphones/', SmartphoneListAPIView.as_view(),
            name='smartphones_list'),
    path('smartphones/<str:id>/', SmartphoneDetailAPIView.as_view(),
            name='smartphone_detail'),
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks_list'),
    path('notebooks/<str:id>/', NotebookDetailAPIView.as_view(),
            name='notebook_detail'),
    path('customers/', CustomersListAPIView.as_view(), name='customers_list')
]
