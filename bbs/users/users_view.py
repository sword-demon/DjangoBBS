from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from bbs.forms.user_form import UpdateUserForm, UpdateUserPhone, UpdatePasswordForm, UpdateAvatarForm
from bbs.models import Users, Topics, Likes, Comments
from djangoBBS import dev, settings
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
        topics = Topics.objects.filter(user_id=request.user.id).all()
        for topic in topics:
            topic.like_num = Likes.objects.filter(topic_id=topic.id, is_like=1).count()
            topic.hate_num = Likes.objects.filter(topic_id=topic.id, is_like=0).count()
            topic.comment_num = Comments.objects.filter(topic_id=topic.id).count()
        my = Users.objects.filter(id=request.user.id).first()
        return render(request, 'users/user_center.html', {"topics": topics, "my": my})

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
    """
    用户修改头像
    """

    @method_decorator(check_login, name='get')
    def get(self, request):
        return render(request, 'users/user_center/edit_avatar.html')

    @method_decorator(check_login, name='post')
    def post(self, request):
        update_avatar_form = UpdateAvatarForm(request.POST, request.FILES)
        if update_avatar_form.is_valid():
            user = request.user
            user.avatar = update_avatar_form.cleaned_data.get("avatar")
            user.save()

            return Show.success("上传成功")
        else:
            return Show.fail("网络异常,图片上传失败,请稍后再试")


class UserBindPhone(UserCenter):
    """
    用户绑定手机
    """

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
    """
    用户修改密码
    """

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
