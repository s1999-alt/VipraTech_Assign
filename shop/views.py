from django.shortcuts import render, redirect
from .models import Product, Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
  products = Product.objects.all()
  orders = Order.objects.filter(paid=True)

  context = {
    "products": products,
    "orders": orders,
    "stripe_public_key": settings.STRIPE_PUBLIC_KEY
  }
  return render(request, "index.html", context)


@csrf_exempt
def create_checkout_session(request):
  if request.method =='POST':
    product_id = request.POST.get("product_id")
    quantity = int(request.POST.get("quantity"))

    product = Product.objects.get(id=product_id)
    total = product.price * quantity

    session = stripe.checkout.Session.create(
      payment_method_types=["card"],
      line_items=[{
        "price_data": {
          "currency": "inr",
          "product_data": {"name": product.name},
          "unit_amount" : int(product.price * 100)
        },
        "quantity": quantity,
      }],
      mode="payment",
      success_url=request.build_absolute_uri("/success?session_id={CHECKOUT_SESSION_ID}"),
      cancel_url=request.build_absolute_uri("/"),
    )

    Order.objects.create(
      product=product,
      quantity=quantity,
      total_amount=total,
      payment_id=session.id,
    )

    return redirect(session.url, code=303)
  









