from django.contrib import messages
from django.core.validators import MinValueValidator
from django.forms import forms, CharField, FloatField
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Mauricio Escudero Restrepo",
        })
        return context


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            "email": "lmario1@eafit.edu.co",
            "phone": "+5731955555555",
            "address": "123 evergreen st"
        })
        return context


class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV"},
        {"id": "2", "name": "iPhone", "description": "Best iPhone"},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast"},
        {"id": "4", "name": "Glasses", "description": "Best Glasses"}
    ]


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        if id:
            product = Product.products[int(id) - 1]
            if not product:
                return HttpResponseRedirect("/home")
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product information"
        viewData["product"] = product
        return render(request, self.template_name, viewData)


class ProductForm(forms.Form):
    name = CharField(required=True)
    price = FloatField(required=True, validators=[MinValueValidator(0.01)], error_messages={"invalid": "Este valor debe ser positivo."})


class ProductCreateView(View):
    template_name = 'products/create.html'


    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)


    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your form was submitted successfully!")
            return HttpResponseRedirect(reverse('home'))
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
