from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from users.models import Profile
from .forms import RegisterForm, UserForm, DepositForm
from books.models import Borrow
from django.core.mail import send_mail
from django.conf import settings

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        return render(request, 'users/login.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        borrows = Borrow.objects.filter(user=request.user)
        context = {
            'user_form': user_form,
            'borrows': borrows,
        }
        return render(request, 'users/profile.html', context)
    
    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('profile')
        borrows = Borrow.objects.filter(user=request.user)
        context = {
            'user_form':user_form,
            'borrows': borrows
        }
        return render(request, 'users/profile.html', context)
    
    @login_required
    def profile(request):
        profile = Profile.objects.get(user=request.user)
        return render(request, 'users/profile.html', {'profile': profile})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
    
@method_decorator(login_required, name='dispatch')
class BorrowHistoryView(View):
    def get(self, request):
        borrows = Borrow.objects.filter(user=request.user)
        context = {
            'borrows': borrows,
        }
        return render(request, 'users/profile.html', context)

@method_decorator(login_required, name='dispatch')
class DepositView(View):
    def get(self, request):
        form = DepositForm()
        return render(request, 'users/deposit_money.html', {'form': form})

    def post(self, request):
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile = Profile.objects.get(user=request.user)
            profile.balance += amount
            profile.save()

            # Send confirmation email
            send_mail(
                'Deposit Confirmation',
                f'You have successfully deposited {amount} to your account.',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )

            return redirect('profile')
        return render(request, 'users/deposit.html', {'form': form})
