from django.urls import path
from bbs import views
from bbs.users import users_view

urlpatterns = [
    # 个人中心
    path('user_center/', users_view.UserCenter.as_view(), name='user_center'),
    path('users/settings/edit/', users_view.UserProfile.as_view(), name='edit_profile'),
    path('users/settings/update/', users_view.UserProfile.post, name='upload_profile'),
    path('users/settings/edit_avatar/', users_view.UserAvatar.as_view(), name='edit_avatar'),
    path('users/settings/edit_phone/', users_view.UserBindPhone.as_view(), name='edit_phone'),
    path('users/settings/edit_password/', users_view.UserChangePassword.as_view(), name='edit_password'),
]
