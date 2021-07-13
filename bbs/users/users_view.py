from django.shortcuts import render, redirect

# Create your views here.
from bbs.forms.user_form import RegisterForm, LoginForm
from bbs.models import Users
from utils.json_response import Show


def users(request, user_id):
    return render(request, 'users/user_center.html')


def edit_profile(request, user_id):
    return render(request, 'users/user_center/edit_profile.html')


def edit_avatar(request):

    return render(request, 'users/user_center/edit_avatar.html')
