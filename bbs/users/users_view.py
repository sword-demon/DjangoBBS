from django.shortcuts import render, redirect

# Create your views here.
from bbs.forms.user_form import RegisterForm, LoginForm
from bbs.models import Users
from utils.json_response import Show


def users(request, id):
    return render(request, 'users/user_center.html')
