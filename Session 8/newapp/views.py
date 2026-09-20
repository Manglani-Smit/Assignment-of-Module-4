from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def signup(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            msg="Email already exists"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                )
                msg="Signup successful"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Passwords do not match"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')

def login(request):
    if request.method == 'POST':
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email']=user.email
                request.session['username']=user.fname
                msg="Login successful"
                return render(request,'index.html',{'msg':msg})
            else:
                msg="Invalid email or password"
                return render(request,'login.html',{'msg':msg})
        except:
            msg="Email does not exist"
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'login.html')

def logout(request):
        try:
            del request.session['email']
            del request.session['username']
            return render(request,'login.html')
        except:
            return render(request,'login.html')