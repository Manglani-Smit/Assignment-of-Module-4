import json
import random
import stripe
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import User, Product, Cart, IPLTicketOrder

# Stripe API Key
stripe.api_key = settings.STRIPE_SECRET_KEY  # Yahan apni Stripe Secret Key dalein


def index(request):
    return render(request,'index.html')
# ------------------ AUTHENTICATION (SIGNUP / LOGIN / LOGOUT) ------------------
def signup(request):
    if request.method == "POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email already exist"
            return render(request, 'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                )
                msg="Signup Successful"
                return render(request, 'signup.html', {'msg': msg})
            else:
                msg="Password did not match"
                return render(request, 'signup.html', {'msg': msg})
    else:
        return render(request,'signup.html')


def user_login(request):
        if request.method == "POST":
            try:
                user = User.objects.get(email=request.POST['email'])
                if user.password == request.POST['password']:
                    request.session['email'] = user.email
                    request.session['fname'] = user.fname
                    return redirect('index')
                else:
                    msg = "Incorrect Credentials"
                    return render(request, 'login.html', {'msg': msg})
            except:
                msg = "Email does not exist"
                return render(request, 'login.html', {'msg': msg})
        else:
            return render(request, 'login.html')
def user_logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def pay_ticket(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = f"IPL-{random.randint(100000, 999999)}"

        IPLTicketOrder.objects.create(
            name=name,
            email=email,
            amount=amount,
            order_id=order_id,
            gateway='Paytm'
        )

        # Q2: Paytm Sandbox simulation params
        paytm_params = {
            'MID': 'YOUR_PAYTM_MID',
            'ORDER_ID': order_id,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'CALLBACK_URL': request.build_absolute_uri('/payment-callback/'),
        }
        return render(request, 'paytm_redirect.html', {'paytm_params': paytm_params})

    return render(request, 'pay_ticket.html')


@csrf_exempt
def payment_callback(request):
    # Q3: Handle callback from Paytm
    if request.method == 'POST':
        order_id = request.POST.get('ORDERID')
        resp_code = request.POST.get('RESPCODE')

        ticket = IPLTicketOrder.objects.filter(order_id=order_id).first()
        if resp_code == '01':  # '01' is Paytm TXN_SUCCESS code
            if ticket:
                ticket.status = 'Success'
                ticket.save()
            return render(request, 'paytm_status.html', {'status': 'Success', 'order_id': order_id})
        else:
            if ticket:
                ticket.status = 'Failed'
                ticket.save()
            return render(request, 'paytm_status.html', {'status': 'Failed', 'order_id': order_id})

    return redirect('pay_ticket')


# ------------------ Q4: ZOMATO-STYLE FOOD ORDER & STRIPE CHECKOUT ------------------
def food_order(request):
    if 'email' not in request.session:
        return redirect('login')

    user = User.objects.filter(email=request.session['email']).first()

    # Sample dish listing / cart generation
    product, _ = Product.objects.get_or_create(
        name="Butter Chicken with Naan",
        defaults={'price': 350.00, 'description': "Special North Indian Thali"}
    )
    cart_item, _ = Cart.objects.get_or_create(
        user=user,
        product=product,
        payment_status=False,
        defaults={'quantity': 1, 'total_price': 350.00}
    )

    net_price = int(cart_item.total_price)
    return render(request, 'food_order.html', {
        'user': user,
        'dish': product,
        'net_price': net_price
    })


@csrf_exempt
def create_checkout_session(request):
    domain_url = request.build_absolute_uri('/')[:-1]
    amount = int(json.load(request)['post_data'])
    final_amount = amount * 100
    user = User.objects.get(email=request.session['email'])
    user_name = f"{user.fname} {user.lname}"
    user_address = f"{user.address}"
    user_mobile = f"{user.mobile}"

    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': final_amount,
                'product_data': {
                    'name': 'Monarch Kicks Order',
                    'description': f'''Customer:{user_name},\n\n
                Address:{user_address},\n
                Mobile:{user_mobile}''',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=domain_url + f'/success/?user_email={user.email}',
        cancel_url=domain_url + '/cancel/',
        customer_email=user.email,
        shipping_address_collection={
            'allowed_countries': ['IN'],
        }
    )
    return JsonResponse({'id': session.id})


def success(request):
    user_email = request.GET.get('user_email') or request.session.get('email')

    user = None
    if user_email:
        user = User.objects.filter(email=user_email).first()
        request.session['email'] = user_email

    carts = []
    total_amount = 0

    if user:
        unpaid_carts = list(Cart.objects.filter(user=user, payment_status=False).select_related('product'))
        if unpaid_carts:
            carts = unpaid_carts
            for i in carts:
                total_amount += i.total_price
                i.payment_status = True
                i.save()
        else:
            carts = list(
                Cart.objects.filter(user=user, payment_status=True).select_related('product').order_by('-id')[:5])
            total_amount = sum(i.total_price for i in carts)

    order_id = random.randint(10000, 99999)

    return render(request, 'success.html', {
        'user': user,
        'carts': carts,
        'total_amount': total_amount,
        'order_id': order_id,
    })


def cancel(request):
    return render(request, 'cancel.html')


# ------------------ Q5: PAYPAL SANDBOX INTEGRATION ------------------
"""
[PROMPT TO COPILOT / CHATGPT]:
"Write Python code to integrate PayPal payment processing for a ticket checkout scenario in a web framework."

[GENERATED & ADAPTED CODE BELOW]:
"""


def paypal_ticket_pay(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        amount = request.POST.get('amount')
        order_id = f"PAYPAL-IPL-{random.randint(100000, 999999)}"

        IPLTicketOrder.objects.create(
            name=name,
            email=email,
            amount=amount,
            order_id=order_id,
            gateway='PayPal'
        )

        paypal_dict = {
            'business': 'sb-test-merchant@business.example.com',
            'amount': amount,
            'item_name': f'IPL Match Ticket for {name}',
            'invoice': order_id,
            'currency_code': 'USD',
            'return_url': request.build_absolute_uri('/paypal-return/'),
            'cancel_url': request.build_absolute_uri('/cancel/'),
        }
        return render(request, 'paypal_form.html', {'paypal_dict': paypal_dict})

    return render(request, 'paypal_ticket_pay.html')


def paypal_return(request):
    return render(request, 'paytm_status.html', {'status': 'Success (PayPal)', 'order_id': 'Verified'})