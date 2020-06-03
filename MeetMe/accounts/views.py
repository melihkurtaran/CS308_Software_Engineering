from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.forms import inlineformset_factory
from django.core.mail import send_mail
from MeetMe.settings import EMAIL_HOST_USER

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_text, force_bytes
from .tokens import account_activation_token

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            email = form.cleaned_data.get('email')
            form.is_active = False
            user.save()
            current_site = get_current_site(request)
            """
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password1)
            auth.login(request, user)
            """
            subject = 'Please Activate Your Account'
            message = render_to_string('accounts/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # method will generate a hash value with user related data
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            #messages.success(request, f'Account Created for {username}')
            return redirect('register')
        try:
            form.password1.validate
        except:
             messages.warning(request, f'Password is too weak or does not match')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    # checking if the user exists, if the token is valid.
    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true 
        user.is_active = True
        # set signup_confirmation true
        user.profile.signup_confirmation = True
        user.save()
        auth.login(request, user)
        return redirect('home')
    else:
        return render(request, 'activation_invalid.html')

def login(request):
     if request.method=='POST':
         username=request.POST['username']
         password=request.POST['password']
         user=auth.authenticate(username=username,password=password)
         if user is not None:
             auth.login(request,user)
             print('User login')
             return redirect('/eventCalendar/calendar')
         else:
             messages.info(request,'Invalid login please check your username and password')
             return redirect('login')
     else:
        return render(request,'accounts/login.html')
        
def logout(request):
    auth.logout(request)
    return render(request, 'accounts/logout.html')