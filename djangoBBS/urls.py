"""djangoBBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from bbs import views
from djangoBBS import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # 首页
                  path('', views.index, name='home'),
                  # 注册
                  path('reg/', views.reg, name='register'),
                  # 登录
                  path('login/', views.login, name='login'),
                  # 退出
                  path('logout/', views.logout, name='logout'),
                  path('bbs/', include('bbs.urls')),
                  # media配置
                  # re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})

                  # 富文本
                  re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
