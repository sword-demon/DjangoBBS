import logging

from django.contrib import auth
from django.contrib.auth import authenticate
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render, redirect

# Create your views here.
from bbs.forms.user_form import RegisterForm, LoginForm
from bbs.models import Users, Topics
from utils.json_response import Show
# from utils.page import Pagination
from utils.tools import get_ip


def index(request):
    order = request.GET.get("order", "-create_time")
    # 防止用户擅自篡改order的值
    if order not in ["-create_time", "-view_count"]:
        order = "-create_time"
    topics = Topics.objects.all().order_by(order)
    current_page = int(request.GET.get("page", 1))

    paginator = Paginator(topics, 20)

    if paginator.num_pages > 11:
        if current_page - 5 < 1:
            page_range = range(1, 11)
        elif current_page + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 11, paginator.num_pages + 1)
        else:
            page_range = range(current_page - 5, current_page + 5)
    else:
        page_range = paginator.page_range

    try:
        current = paginator.page(current_page)
    except EmptyPage as e:
        current = paginator.page(1)
    return render(request, 'root/index.html',
                  {"topics": current, "order": order, "page_range": page_range, "length": len(topics)})


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


def forget(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        if not username.strip():
            return Show.fail("请输入用户名")
        user_obj = Users.objects.filter(username=username).first()
        if not user_obj:
            return Show.fail("该用户不存在")
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")
        if not password.strip():
            return Show.fail("请输入密码")
        if not confirm_password.strip():
            return Show.fail("请输入确认密码")
        if password != confirm_password:
            return Show.fail("两次密码不一致")

        user_obj.set_password(password)
        user_obj.save()
        return Show.success("密码修改成功,前去登录")

    return render(request, 'auth/forget.html')
