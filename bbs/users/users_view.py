from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from bbs.forms.user_form import UpdateUserForm, UpdateUserPhone, UpdatePasswordForm
from bbs.models import Users
from utils.decorator import check_login
from utils.json_response import Show


class BaseView(View):
    http_method_names = ['get', 'post', 'put', 'delete']


class UserCenter(BaseView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = Users

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center.html')

    def post(self, request):
        pass


class UserProfile(UserCenter):

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center/edit_profile.html')

    @method_decorator(check_login, name='post')
    def post(self, request):
        update_profile_form = UpdateUserForm(request.POST)
        if update_profile_form.is_valid():
            self.model.objects.filter(id=request.POST.get("id")).update(
                **update_profile_form.cleaned_data)
            return Show.success("修改成功")
        else:
            return Show.fail(update_profile_form.errors)


class UserAvatar(UserCenter):

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center/edit_avatar.html')


class UserBindPhone(UserCenter):

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center/edit_phone.html')

    def post(self, request):
        update_phone_form = UpdateUserPhone(request.POST)
        if update_phone_form.is_valid():
            self.model.objects.filter(id=update_phone_form.cleaned_data.get("id")).update(
                **update_phone_form.cleaned_data)
            return Show.success("绑定成功")
        else:
            return Show.fail(update_phone_form.errors)


class UserChangePassword(UserCenter):

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center/edit_password.html')

    @method_decorator(check_login, name='post')
    def post(self, request):
        update_password_form = UpdatePasswordForm(request.POST)
        if update_password_form.is_valid():
            user = request.user
            user.set_password(update_password_form.cleaned_data.get("password"))
            user.save()
            return Show.success("修改成功")
        else:
            return Show.fail(update_password_form.errors)
