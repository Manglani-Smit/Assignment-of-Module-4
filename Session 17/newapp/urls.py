from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('pay/', views.pay_ticket, name='pay_ticket'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
    path('food-order/', views.food_order, name='food_order'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('paypal-pay/', views.paypal_ticket_pay, name='paypal_ticket_pay'),
    path('paypal-return/', views.paypal_return, name='paypal_return'),
]