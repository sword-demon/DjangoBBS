import logging

from django.contrib import auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect

# Create your views here.
from bbs.forms.user_form import RegisterForm, LoginForm
from bbs.models import Users, Topics
from utils.json_response import Show
from utils.tools import get_ip


def index(request):
    order = request.GET.get("order", "-create_time")
    # 防止用户擅自篡改order的值
    if order not in ["-create_time", "-view_count"]:
        order = "-create_time"
    topics = Topics.objects.all().order_by(order)
    # print(topics.query)
    return render(request, 'root/index.html', {"topics": topics, "order": order})


def reg(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        is_valid = form.is_valid()
        if is_valid:
            extra = {
                "last_login_ip": get_ip(request)
            }
            try:
                user = Users.objects.create_user(username=form.cleaned_data.get("username"),
                                                 password=form.cleaned_data.get("password"), **extra)
                if user:
                    return Show.success("注册成功，前去登录!")
                else:
                    return Show.fail()
            except Exception as e:
                print(str(e))
                logging.error(str(e))
                return Show.fail()
        else:
            return Show.fail(form.errors)

    form = RegisterForm()
    return render(request, 'auth/register.html', locals())


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get("username"), password=form.cleaned_data.get("password"))
            if user is not None:
                auth.login(request, user)
                return Show.success("登录成功")
            else:
                return Show.fail("用户名或密码错误")
        else:
            return Show.fail(form.errors)
    form = LoginForm()
    return render(request, 'auth/login.html', locals())


def logout(request):
    """
    退出
    :param request:
    :return:
    """

    request.session.flush()

    return redirect("login")
