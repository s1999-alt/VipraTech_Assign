from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product, Order
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe


def signup_view(request):
  if request.method == "POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('/')
    
  else:
     form = UserCreationForm()
  return render(request, 'signup.html', {'form': form})



def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('/')
  
  else:
     form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})


def index(request):
  products = Product.objects.all()
  orders = Order.objects.filter(user=request.user, paid=True) if request.user.is_authenticated else []

  context = {
    "products": products,
    "orders": orders,
    "stripe_public_key": settings.STRIPE_PUBLIC_KEY
  }
  return render(request, "index.html", context)



stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@login_required(login_url='/login/')
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
      success_url=request.build_absolute_uri('/success') + '?session_id={CHECKOUT_SESSION_ID}',
      cancel_url=request.build_absolute_uri('/cancel'),
    )

    Order.objects.create(
      user=request.user,
      product=product,
      quantity=quantity,
      total_amount=total,
      payment_id=session.id,
    )

    return redirect(session.url, code=303)
  

def success_view(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        return redirect("/")

    try:
        # Fetch latest session info from Stripe
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        print("Stripe Error:", e)
        return redirect("/")

    # Find matching order by payment_id
    order = Order.objects.filter(payment_id=session.id).first()

    # Mark as paid only once
    if order and not order.paid and session.payment_status == "paid":
        order.paid = True
        order.save()

    return redirect("/")


def cancel_view(request):
    context = {
        "message": "Your payment was canceled or failed. Please try again.",
    }
    return render(request, "cancel.html", context)


def logout_view(request):
    logout(request)
    return redirect('/')




