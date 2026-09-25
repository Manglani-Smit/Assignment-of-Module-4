from django.shortcuts import render
from .models import User, InfluencerProfile

def index(request):
    return render(request, 'home.html')

def explore(request):
    return render(request, 'explore.html')

def login(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                try:
                    profile = InfluencerProfile.objects.get(user=user)
                    request.session['profile_picture'] = profile.profile_pic.url
                except:
                    pass
                msg = "Login successful"
                return render(request, 'home.html', {'msg': msg})
            else:
                msg = "Incorrect Password"
                return render(request, 'login.html', {'msg': msg})
        except:
            msg = "Email does not exist"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "Email already exists"
            return render(request, 'signup.html', {'msg': msg})
        except:
            if len(request.POST['mobile']) != 10:
                msg = "Phone number must be exactly 10 digits"
                return render(request, 'signup.html', {'msg': msg})

            if request.POST['password'] == request.POST['cpassword']:
                user = User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    password=request.POST['password']
                )

                try:
                    pic = request.FILES['profile_picture']
                except:
                    pic = None

                InfluencerProfile.objects.create(
                    user=user,
                    display_name=request.POST['fname'],
                    bio=request.POST['address'],
                    phone_number=request.POST['mobile'],
                    profile_pic=pic
                )
                msg = "Signup successful"
                return render(request, 'login.html', {'msg': msg})
            else:
                msg = "Passwords did not match"
                return render(request, 'signup.html', {'msg': msg})
    else:
        return render(request, 'signup.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        del request.session['profile_picture']
    except:
        pass
    msg = "Logout successful"
    return render(request, 'login.html', {'msg': msg})

def change_password(request):
    if request.method == 'POST':
        user = User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['cnew_password']:
                if user.password != request.POST['new_password']:
                    user.password = request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    try:
                        del request.session['profile_picture']
                    except:
                        pass
                    msg = "Password changed successful"
                    return render(request, 'login.html', {'msg': msg})
                else:
                    msg = "Password Can't be Old Password"
                    return render(request, 'change-password.html', {'msg': msg})
            else:
                msg = "New Password And Confirm Password Doesn't Match"
                return render(request, 'change-password.html', {'msg': msg})
        else:
            msg = "Old Password Does not Match"
            return render(request, 'change-password.html', {'msg': msg})
    else:
        return render(request, 'change-password.html')

def profile(request):
    user = User.objects.get(email=request.session['email'])
    profile = InfluencerProfile.objects.get(user=user)

    if request.method == 'POST':
        if len(request.POST['mobile']) != 10:
            msg = "Phone number must be exactly 10 digits"
            return render(request, 'profile.html', {'msg': msg, 'user': user, 'profile': profile})

        user.fname = request.POST['fname']
        user.lname = request.POST['lname']
        user.save()

        profile.display_name = request.POST['fname']
        profile.phone_number = request.POST['mobile']
        profile.bio = request.POST['address']

        try:
            profile.profile_pic = request.FILES['profile_picture']
        except:
            pass

        profile.save()

        try:
            request.session['profile_picture'] = profile.profile_pic.url
        except:
            pass

        msg = "Profile Updated Successfully"
        return render(request, 'profile.html', {'msg': msg, 'user': user, 'profile': profile})
    else:
        return render(request, 'profile.html', {'user': user, 'profile': profile})