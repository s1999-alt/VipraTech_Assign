from django.urls import path, include
from . import views


urlpatterns = [
  path('', views.index, name='index'),
  path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
  path('success', views.success_view, name='success'),
]
