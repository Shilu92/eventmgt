from django.urls import path

from . import views
from .views import login_user, logout_view
from eventapp.views import home

urlpatterns = [

    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('login/', login_user, name='login'),
    path('welcome',views.welcome, name = 'welcome'),
    path('home', home, name='home'),
    path('logout/', logout_view, name='logout'),
]