from django.urls import path
from bbs import views
from bbs.users import users_view

urlpatterns = [
    # 个人中心
    path('user_center/<int:id>/', users_view.users, name='user_center')
]
