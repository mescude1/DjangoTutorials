from django.urls import path
from .views import HomePageView, AboutPageView, ProductShowView, ProductIndexView, ProductCreateView

urlpatterns = [
   path("", HomePageView.as_view(), name='home'),
   path('about/', AboutPageView.as_view(), name='about'),
   path('products/', ProductIndexView.as_view(), name='index'),
   path('products/detail/<str:id>/', ProductShowView.as_view(), name='show'),
   path('products/create/', ProductCreateView.as_view(), name='form'),
]