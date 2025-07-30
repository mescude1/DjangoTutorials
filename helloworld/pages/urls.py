from django.urls import path
from .views import homePageView

urlpatters = [
   path("", homePageView, name='home')
]