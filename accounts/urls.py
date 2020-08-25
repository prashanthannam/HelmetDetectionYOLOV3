from django.contrib import admin
from django.urls import path
from accounts.views import *

app_name='accounts'
urlpatterns=[
    path('signup',signup_view,name='signup'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout')
]