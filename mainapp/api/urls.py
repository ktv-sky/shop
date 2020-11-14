from django.urls import path

from .api_views import (CategoryListAPIView, NotebookListAPIView,
                        SmartphoneListAPIView)

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('smartphones/', SmartphoneListAPIView.as_view(), name='smartphones'),
    path('notebooks/', NotebookListAPIView.as_view(), name='notebooks')
]
