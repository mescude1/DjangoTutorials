from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import forms, ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from .models import Product


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


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        view_data = {}
        if id:
            try:
                product_id = int(id)
                if product_id < 1:
                    raise ValueError("Invalid product id")
                product = get_object_or_404(Product, pk=product_id)

                view_data["title"] = product.name + " - Online Store"
                view_data["subtitle"] = product.name + " - Product information"
                view_data["product"] = product
                return render(request, self.template_name, view_data)
            except (ValueError, IndexError):
                return HttpResponseRedirect("/home")
        else:
            return HttpResponseRedirect("/home")


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price"]

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price


class ProductCreateView(View):
    template_name = 'products/create.html'


    def get(self, request):
        form = ProductForm()
        view_data = {"title": "Create product", "form": form}
        return render(request, self.template_name, view_data)


    def post(self, request):
        form = ProductForm(request.POST)
        view_data = {}
        if form.is_valid():
            messages.success(request, "Your form was submitted successfully!")
            return HttpResponseRedirect(reverse('home'))
        else:
            view_data["title"] = "Create product"
            view_data["form"] = form
            return render(request, self.template_name, view_data)


class ProductListView(ListView):
    model = Product
    template_name = 'products/products_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Products - Online Store"
        context["subtitle"] = "List of products"
        return context


class CartView(View):
    template_name = 'cart/index.html'
    def get(self, request):
        products = Product.objects.all()
        cart_products = {}

        cart_product_data = request.session.get('cart_product_data')

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        view_data = {
            'title': 'Cart - Online Store',
            'subtitle': 'Shopping cart',
            'products': products,
            'cart_products': cart_products
        }

        return render(request, self.template_name, view_data)

    def post(self, request, product_id):
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data['product_id'] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')

class CartRemoveAllView(View):

    def post(self, request):
        cart_products = request.session.get('cart_product_data', {})
        cart_products.pop_all()
        request.session['cart_product_data'] = cart_products

        return redirect('cart_index')