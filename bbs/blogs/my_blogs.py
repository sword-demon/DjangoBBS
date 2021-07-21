import time

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
        topics = Topics.objects.filter(user__username=username).all()
        return render(request, 'my_blogs/blog_center.html', locals())


class CreateTopic(View):

    @method_decorator(check_login, name='get')
    def get(self, request):
        create_topic_form = CreateTopicForm()
        return render(request, 'my_blogs/create.html', {"create_topic_form": create_topic_form})

    @method_decorator(check_login, name='post')
    def post(self, request):
        create_topic_form = CreateTopicForm(request.POST)
        if create_topic_form.is_valid():
            # print(create_topic_form.cleaned_data['body'])
            new_record = create_topic_form.save(commit=False)
            new_record.user = request.user
            new_record.create_time = time.time()
            new_record.save()

            return Show.success("添加成功")
        else:
            # print(create_topic_form.errors)
            return Show.fail(create_topic_form.errors)
