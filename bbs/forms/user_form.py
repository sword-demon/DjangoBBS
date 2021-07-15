from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
import re

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


class UpdateUserForm(forms.Form):
    id = forms.IntegerField(required=True, label='ID', error_messages={"required": "ID参数缺失"})
    nickname = forms.CharField(max_length=50, label='昵称', error_messages={"max_length": "昵称最长不超过50个字符"}, required=False)
    sex = forms.IntegerField(required=True, error_messages={"required": "请选择性别"}, label='性别')
    github = forms.CharField(max_length=255, error_messages={"max_length": "链接长度不超过255个字符"}, required=False,
                             label='Github')
    email = forms.CharField(max_length=64, error_messages={"max_length": "邮箱长度不超过64个字符", "required": "邮箱不能为空"},
                            required=True, label='邮箱')
    first_name = forms.CharField(max_length=30, required=False, label='姓')
    last_name = forms.CharField(max_length=150, required=False, label='名')
    birthday = forms.DateTimeField(required=False, label='生日')
    sign = forms.CharField(max_length=128, error_messages={"max_length": "个性签名不超过128个字符"}, required=False, label='个性签名')
    introduction = forms.CharField(required=False, label='个人介绍')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return email
        else:
            raise ValidationError("邮箱格式错误")


class UpdateUserPhone(forms.Form):
    id = forms.IntegerField(required=True, label='ID', error_messages={"required": "ID参数缺失"})
    mobile = forms.CharField(max_length=11, label='手机号码', required=True,
                             error_messages={"required": "手机号码不能为空", "max_length": "手机号码长度为11位"})

    def clean(self):
        mobile = self.cleaned_data.get("mobile")
        ret = re.match(r"^1[35678]\d{9}$", mobile)
        if ret:
            return self.cleaned_data
        else:
            raise ValidationError("手机号码格式错误")


class UpdatePasswordForm(forms.Form):
    id = forms.IntegerField(required=True, label='ID', error_messages={"required": "ID参数缺失"})
    password = forms.CharField(max_length=128, label='密码', required=True,
                               error_messages={"required": "密码不能为空", "max_length": "密码长度为128位"})
    confirm_password = forms.CharField(max_length=128, label='确认密码', required=True,
                                       error_messages={"required": "确认密码不能为空", "max_length": "确认密码长度为128位"})

    def clean(self):
        pwd = self.cleaned_data.get("password")
        confirm_pwd = self.cleaned_data.get("confirm_password")
        if pwd == confirm_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")


class UpdateAvatarForm(forms.Form):
    avatar = forms.FileField(max_length=255)

    def clean(self):
        return self.cleaned_data
