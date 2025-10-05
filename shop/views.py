from django.shortcuts import render, redirect
from .models import Product, Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt



def index(request):
  products = Product.objects.all()
  orders = Order.objects.filter(paid=True)

  context = {
    "products": products,
    "orders": orders,
    "stripe_public_key": settings.STRIPE_PUBLIC_KEY
  }
  return render(request, "index.html", context)

