from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import User, PhoneOTP
import random
import requests
import os

# ----------------- API KEYS -----------------

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
FAST2SMS_API_KEY = os.getenv('FAST2SMS_API_KEY')
# ---------------------------------------------

def home(request):
    return render(request, 'home.html')

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


def user_logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


# Q2: Mailgun Registration & Welcome Email (Custom User Model)
def send_mailgun_welcome_email(first_name, recipient_email):
    endpoint = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    auth = ("api", MAILGUN_API_KEY)
    data = {
        "from": f"Support Team <mailgun@{MAILGUN_DOMAIN}>",
        "to": [recipient_email],
        "subject": "Welcome to Our Platform!",
        "text": f"Hello {first_name},\n\nThank you for registering with us. We are happy to have you on board!\n\nBest Regards,\nTeam"
    }
    try:
        response = requests.post(endpoint, auth=auth, data=data)
        return response.status_code == 200
    except Exception:
        return False

def register_view(request):
    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST['email'])
            msg = "Email already exists"
            return render(request, 'signup.html', {'msg': msg})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    password=request.POST['password'],
                )
                msg = "Signup successful"
                return render(request, 'login.html', {'msg': msg})
            else:
                msg = "Passwords did not match"
                return render(request, 'signup.html', {'msg': msg})
    else:
        return render(request, 'signup.html')


# Q3: Forgot Password Logic (Fast2SMS 'q' route)
def forgot_password(request):
    if request.method == 'POST':
        try:
            user = User.objects.filter(mobile=request.POST['mobile']).first()
            if not user:
                raise Exception("User not found")

            otp = random.randint(1000, 9999)
            mobile = str(user.mobile)
            message = "Hello, Your OTP for Forgot Password is " + str(otp)
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {
                "message": message,
                "route": "q",
                "numbers": mobile,
                "sms_details": "1"
            }
            headers = {
                "accept": "application/json",
                "Authorization": FAST2SMS_API_KEY
            }
            response = requests.get(url, headers=headers, params=querystring)
            print(response.text)
            request.session['mobile'] = user.mobile
            request.session['otp'] = otp
            return render(request, "otp.html")
        except:
            msg = "Mobile Number Not Registered"
            return render(request, "forgot-password.html", {'msg': msg})
    else:
        return render(request, "forgot-password.html")


def verify_otp(request):
    if request.method == 'POST':
        try:
            otp1 = int(request.session['otp'])
            otp2 = int(request.POST['otp'])
            if otp1 == otp2:
                del request.session['otp']
                msg = "Set your new password"
                return render(request, 'new-password.html', {'msg': msg})
            else:
                msg = "Invalid OTP"
                return render(request, 'otp.html', {'msg': msg})
        except:
            return redirect('forgot_password')
    return render(request, 'otp.html')


def new_password(request):
    if 'mobile' not in request.session:
        return redirect('forgot_password')

    msg = ""
    if request.method == 'POST':
        npwd = request.POST.get('new_password')
        cnpwd = request.POST.get('cnew_password')

        if npwd == cnpwd:
            user = User.objects.filter(mobile=request.session['mobile']).first()
            if user:
                user.password = npwd
                user.save()
                del request.session['mobile']
                msg = "Password Changed Successfully! Please Login."
                return render(request, 'new-password.html', {'msg': msg, 'success': True})
            else:
                msg = "User not found!"
                return render(request, 'new-password.html', {'msg': msg})
        else:
            msg = "New Password and Confirm Password do not match!"
            return render(request, 'new-password.html', {'msg': msg})

    return render(request, 'new-password.html')


# Q4: Model-Based OTP Store & Expiry Verification
def request_otp(request):
    msg = ""
    if request.method == "POST":
        mobile = request.POST.get('mobile')
        otp = str(random.randint(1000, 9999))

        PhoneOTP.objects.create(mobile=mobile, otp=otp)

        url = "https://www.fast2sms.com/dev/bulkV2"
        querystring = {
            "message": f"Your verification OTP is {otp}",
            "route": "q",
            "numbers": mobile,
            "sms_details": "1"
        }
        headers = {
            "accept": "application/json",
            "Authorization": FAST2SMS_API_KEY
        }
        try:
            res = requests.get(url, headers=headers, params=querystring)
            print(res.text)
            return render(request, 'verify_stored_otp.html', {
                'mobile': mobile,
                'msg': f"OTP sent to {mobile}. Please enter code below."
            })
        except Exception as e:
            msg = f"Error sending SMS: {str(e)}"

    return render(request, 'request_otp.html', {'msg': msg})


def verify_stored_otp(request):
    msg = ""
    status = False
    mobile = request.POST.get('mobile')
    entered_otp = request.POST.get('otp')

    if request.method == "POST":
        record = PhoneOTP.objects.filter(mobile=mobile, is_verified=False).order_by('-created_at').first()

        if record:
            if not record.is_valid():
                msg = "OTP has expired! Please request a new one."
            elif record.otp == entered_otp:
                record.is_verified = True
                record.save()
                msg = "Mobile Number Verified Successfully via Model!"
                status = True
            else:
                msg = "Invalid OTP! Please try again."
        else:
            msg = "No OTP request found for this mobile number."

    return render(request, 'verify_stored_otp.html', {'msg': msg, 'status': status, 'mobile': mobile})