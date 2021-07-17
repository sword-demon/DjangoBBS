from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from bbs.forms.topic_form import CreateTopicForm
from bbs.models import Topics, Users
from djangoBBS import dev, settings
from utils.decorator import check_login
from utils.json_response import Show


# from utils.mixin import LoginRequiredMixin


class MyBlog(View):

    @method_decorator(check_login, name='get')
    def get(self, request, username):
        # 根据用户名查询该用户的一些数据
        nums = [i for i in range(20)]
        return render(request, 'my_blogs/blog_center.html', locals())


class CreateTopic(View):

    @method_decorator(check_login, name='get')
    def get(self, request):
        create_topic_form = CreateTopicForm()
        return render(request, 'my_blogs/create.html', {"create_topic_form": create_topic_form})

    @method_decorator(check_login, name='post')
    def post(self, request):
        print(request.POST)
        create_topic_form = CreateTopicForm()

        return Show.success()
