from django.urls import path
from bbs import views

urlpatterns = [
    # 个人中心
    path('user_center/<id:int>/', views.users, name='user_center')
]
