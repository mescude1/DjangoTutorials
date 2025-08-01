from django.urls import path
from .views import homePageView, AboutPageView, ProductShowView, ProductIndexView, ProductCreateView

urlpatters = [
   path("", homePageView, name='home'),
   path('about/', AboutPageView.as_view(), name='about'),
   path('products/', ProductIndexView.as_view(), name='index'),
   path('products/<str:id>', ProductShowView.as_view(), name='show'),
   path('products/create', ProductCreateView.as_view(), name='form'),
]