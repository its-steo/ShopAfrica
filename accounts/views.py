from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
import time
from .forms import RegisterForm
from django.template.loader import render_to_string

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # ✅ Send styled HTML email
            subject = 'Welcome to ShopEase!'
            html_message = render_to_string('accounts/email/account_created.html', {
                'user': user,
            })
            email = EmailMessage(
                subject,
                html_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=True)

            # ✅ Add success message
            messages.success(request, 'Account created successfully! Redirecting to login...')

            # ✅ Render same template with redirect hint
            return render(request, 'accounts/register.html', {
                'form': RegisterForm(),  # Reset form
                'redirect_to_login': True
            })
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Update this if 'home' is not defined
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def cart_view(request):
    return render(request,'accounts/cart.html')

@login_required
def home(request):
    return render(request, 'accounts/home.html')