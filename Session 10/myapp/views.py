from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.
def index(request):
    return render(request,'index.html')


def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks']
        )
        msg = "Contact is Saved Successfully"
        contacts = Contact.objects.all().order_by("-id")[:3]
        return render(request, 'contact.html', {'msg': msg, 'contacts': contacts})

    else:
        contacts = Contact.objects.all().order_by("-id")[:3]
        return render(request, 'contact.html', {'contacts': contacts})

def login(request):
    if request.method == "POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                return render(request, 'index.html')
            else:
                msg="Incorrect Credentials"
                return render(request, 'login.html', {'msg': msg})
        except:
            msg="Email does not exist"
            return render(request, 'login.html', {'msg': msg})
    else:
        msg="Login Failed"
        return render(request,'login.html',{'msg': msg})

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

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')

def forgot_password(request):
    if request.method == "POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            address=request.POST['email']
            subject="OTP For Password Reset"
            message="Your OTP for Forgot Password is "+str(otp)+"."
            send_mail(subject,message,settings.EMAIL_HOST_USER,[address,])
            request.session['email_to'] = user.email
            request.session['otp'] = otp
            return render(request, 'otp.html')
        except:
            msg="Email does not exist"
            return render(request, 'forgot-password.html', {'msg': msg})
    else:
        return render(request,'forgot-password.html')

def verify_otp(request):
    otp1=int(request.session['otp'])
    otp2=int(request.POST['otp'])
    if otp1 == otp2:
        del request.session['otp']
        msg="Set your new password"
        return render(request, 'new-password.html', {'msg': msg})
    else:
        msg="Invalid OTP"
        return render(request, 'otp.html', {'msg': msg})

def new_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(email=request.session['email_to'])
        user.password=request.POST['new_password']
        user.save()
        del request.session['email_to']
        msg="Password Updated Successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg="New Password & Confirm Password not match"
        return render(request, 'new-password.html', {'msg': msg})

def change_password(request):
    if request.method == "POST":
        user=User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['cnew_password']:
                if user.password != request.POST['new_password']:
                    user.password = request.POST['new_password']
                    user.save()
                    del request.session['email']
                    del request.session['fname']
                    msg="Password Changed Successfully"
                    return render(request, 'login.html',{'msg': msg})
                else:
                    msg="New Password Cant be From Old Password"
                    return render(request, 'new-password.html',     {'msg': msg})
            else:
                msg="New Password and Confirm New Password not match"
                return render(request, 'new-password.html', {'msg': msg})
        else:
            msg="Old Password is not match"
            return render(request, 'new-password.html', {'msg': msg})
    else:
        return render(request,'change-password.html')
