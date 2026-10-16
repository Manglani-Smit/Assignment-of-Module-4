from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from .models import User, Order, Product, MovieReview, Playlist


def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'email' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)

    return wrapper

@custom_login_required
def my_orders(request):
    try:
        user = User.objects.get(email=request.session['email'])
        orders = Order.objects.filter(user=user).order_by('-order_date')
        return render(request, 'my_orders.html', {'user': user, 'orders': orders})
    except User.DoesNotExist:
        return redirect('login')


@custom_login_required
def post_product(request):
    user = User.objects.get(email=request.session['email'])

    # Check if user is Seller
    if user.usertype != 'Seller':
        return HttpResponseForbidden("Permission Denied: Only Sellers can post products!")

    if request.method == 'POST':
        pname = request.POST.get('product_name')
        price = request.POST.get('price')
        desc = request.POST.get('description')

        Product.objects.create(
            seller=user,
            product_name=pname,
            price=price,
            description=desc
        )
        msg = "Product Added Successfully!"
        return render(request, 'post_product.html', {'msg': msg})

    return render(request, 'post_product.html')


@custom_login_required
def movie_reviews(request):
    user = User.objects.get(email=request.session['email'])
    reviews = MovieReview.objects.all()

    if request.method == 'POST':
        if user.group_name != 'MovieCritic':
            return HttpResponseForbidden("Access Denied: MovieFan can only view reviews, cannot post!")

        mname = request.POST.get('movie_name')
        rtext = request.POST.get('review_text')
        rating = request.POST.get('rating')

        MovieReview.objects.create(
            user=user,
            movie_name=mname,
            review_text=rtext,
            rating=rating
        )
        return redirect('movie_reviews')

    return render(request, 'movie_reviews.html', {
        'user': user,
        'reviews': reviews,
        'is_critic': user.group_name == 'MovieCritic'
    })


@custom_login_required
def dashboard(request):
    user = User.objects.get(email=request.session['email'])

    # Check role and redirect
    if user.usertype == 'Seller':
        return redirect('seller_dashboard')
    elif user.usertype == 'Buyer':
        return redirect('buyer_dashboard')
    else:
        return render(request, 'default_dashboard.html', {'user': user})


@custom_login_required
def seller_dashboard(request):
    user = User.objects.get(email=request.session['email'])
    if user.usertype != 'Seller':
        return redirect('dashboard')

    products = Product.objects.filter(seller=user)
    return render(request, 'seller_dashboard.html', {'user': user, 'products': products})


@custom_login_required
def buyer_dashboard(request):
    user = User.objects.get(email=request.session['email'])
    if user.usertype != 'Buyer':
        return redirect('dashboard')

    orders = Order.objects.filter(user=user)
    return render(request, 'buyer_dashboard.html', {'user': user, 'orders': orders})

@custom_login_required
def playlist_view(request):
    user = User.objects.get(email=request.session['email'])
    if user.group_name != 'Admin':
        return HttpResponseForbidden("Permission Denied: Only users in the Admin group can view or edit playlists.")
    playlists = Playlist.objects.all()
    return render(request, 'playlist.html', {'playlists': playlists})

def test_login(request, email):
    request.session['email'] = email
    return HttpResponse(f"Logged in as: {email}. Ab kisi bhi page ko test kar sakte ho!")