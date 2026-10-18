from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Restaurant, MovieBookingOTP

def home_dashboard(request):
    user = None
    if 'user_email' in request.session:
        user = User.objects.filter(email=request.session['user_email']).first()
    return render(request, 'dashboard.html', {'user': user})

# Task 1: Zomato Restaurant Search
def search_restaurants(request):
    cuisine = request.GET.get('cuisine', '').strip()
    location = request.GET.get('location', '').strip()

    restaurants = Restaurant.objects.all()
    if cuisine:
        restaurants = restaurants.filter(cuisine__icontains=cuisine)
    if location:
        restaurants = restaurants.filter(location__icontains=location)

    return render(request, 'restaurant_search.html', {
        'restaurants': restaurants,
        'cuisine': cuisine,
        'location': location
    })

# Task 2: Movie App Registration, OTP via Email, Verification
def movie_register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered. Please log in.')
            return redirect('movie_login')

        User.objects.create(name=name, email=email, password=password)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('movie_login')

    return render(request, 'movie_register.html')

def movie_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Direct email & password verification
        user = User.objects.filter(email=email, password=password).first()
        if user:
            otp_obj = MovieBookingOTP.generate_otp(email=email)
            request.session['temp_login_email'] = email
            messages.info(request, f"Simulated SMS/Email: Your OTP is {otp_obj.otp_code} (Valid for 3 mins)")
            return redirect('movie_verify_otp')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'movie_login.html')

def movie_verify_otp(request):
    email = request.session.get('temp_login_email')
    if not email:
        return redirect('movie_login')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp', '').strip()
        otp_entry = MovieBookingOTP.objects.filter(email=email, otp_code=entered_otp).order_by('-created_at').first()

        if otp_entry and otp_entry.is_valid():
            request.session['user_email'] = email
            del request.session['temp_login_email']
            return redirect('movie_dashboard')
        else:
            messages.error(request, 'Invalid or Expired OTP (OTP expires after 3 minutes).')

    return render(request, 'movie_verify_otp.html', {'email': email})

def movie_dashboard(request):
    if 'user_email' not in request.session:
        return redirect('movie_login')
    user = User.objects.filter(email=request.session['user_email']).first()
    return render(request, 'movie_dashboard.html', {'user': user})

def user_logout(request):
    request.session.flush()
    return redirect('home_dashboard')

# Task 3: Flipkart User Profile Management
def flipkart_profile(request):
    if 'user_email' not in request.session:
        messages.error(request, 'Please log in to manage your profile.')
        return redirect('movie_login')

    user = User.objects.filter(email=request.session['user_email']).first()

    if request.method == 'POST':
        user.name = request.POST.get('name', user.name)
        new_email = request.POST.get('email', user.email)
        user.delivery_address = request.POST.get('delivery_address', user.delivery_address)

        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        if new_email != user.email:
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, 'Email already in use.')
                return render(request, 'flipkart_profile.html', {'user': user})
            user.email = new_email
            request.session['user_email'] = new_email

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('flipkart_profile')

    return render(request, 'flipkart_profile.html', {'user': user})

# Task 4: Cab Booking Map Selection
def cab_booking_map(request):
    return render(request, 'cab_booking.html')