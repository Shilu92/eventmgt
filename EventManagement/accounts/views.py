from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import redirect, render

from django.views import View


class UserRegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registration_success')
        return render(request, 'register.html', {'form': form})


def registration_success(request):
    return render(request, 'registration_success.html')


def welcome(request):
    return render(request, 'welcome.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            error_message = "Invalid username or password"
    else:
        error_message = None

    return render(request, 'login.html', {'error_message': error_message})


def logout_view(request):
    logout(request)
    return redirect('signup')
