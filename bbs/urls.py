from django.urls import path
from bbs import views
from bbs.users import users_view

urlpatterns = [
    # 个人中心
    path('user_center/<int:user_id>/', users_view.users, name='user_center'),
    path('users/settings/edit/<int:user_id>/', users_view.edit_profile, name='edit_profile'),
    path('users/settings/edit_avatar/', users_view.edit_avatar, name='edit_avatar')
]
