from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

from bbs.models import Users


class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4, label="用户名", error_messages={"required": "用户名不能为空"})
    password = forms.CharField(min_length=4, label="密码", error_messages={'required': '密码不能为空'},
                               widget=widgets.PasswordInput())
    password_confirmation = forms.CharField(min_length=4, label="确认密码", error_messages={"required": "确认密码不能为空"},
                                            widget=widgets.PasswordInput())

    def clean_username(self):
        """
        进行校验的时候会自动执行此方法
        :return:
        """
        val = self.cleaned_data.get("username")
        ret = Users.objects.filter(username=val)
        if not ret:
            return val
        else:
            raise ValidationError("该用户已注册!")

    def clean(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data.get("password_confirmation")
        if pwd == confirm_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")


class LoginForm(forms.Form):
    username = forms.CharField(min_length=4, label="用户名",
                               error_messages={"required": "用户名不能为空", "min_length": "用户名最小4个字符"})
    password = forms.CharField(min_length=4, label="密码",
                               error_messages={'required': '密码不能为空', "min_length": "最小密码长度为4个字符"},
                               widget=widgets.PasswordInput())
