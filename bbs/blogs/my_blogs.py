import time

from django.db import transaction
from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from bbs.forms.topic_form import CreateTopicForm
from bbs.models import Topics, Users, Tags, Likes, Comments
from djangoBBS import dev, settings
from utils.decorator import check_login
from utils.json_response import Show


# from utils.mixin import LoginRequiredMixin


class MyBlog(View):

    @method_decorator(check_login, name='get')
    def get(self, request, username):
        # 根据用户名查询该用户的一些数据
        topics = Topics.objects.filter(user__username=username).all()
        for topic in topics:
            topic.like_num = Likes.objects.filter(topic_id=topic.id, is_like=1).count()
            topic.hate_num = Likes.objects.filter(topic_id=topic.id, is_like=0).count()
            topic.comment_num = Comments.objects.filter(topic_id=topic.id).count()
        return render(request, 'my_blogs/blog_center.html', locals())


class CreateTopic(View):

    @method_decorator(check_login, name='get')
    def get(self, request):
        create_topic_form = CreateTopicForm()
        return render(request, 'my_blogs/create.html', {"create_topic_form": create_topic_form})

    @method_decorator(check_login, name='post')
    def post(self, request):
        create_topic_form = CreateTopicForm(request.POST)
        tags = request.POST.get("tags")
        tags_list = tags.split(",")
        if create_topic_form.is_valid():
            with transaction.atomic():
                new_record = create_topic_form.save(commit=False)
                new_record.user = request.user
                new_record.create_time = time.time()
                new_record.save()

                if tags:
                    tags_insert_batch = []
                    for i in tags_list:
                        tags_insert_batch.append(Tags(title=i, user_id=request.user.id, topic_id=new_record.id))

                    Tags.objects.bulk_create(tags_insert_batch)

            return Show.success("添加成功")
        else:
            return Show.fail(create_topic_form.errors)


def like(request):
    if request.method == "POST":
        topic_id = request.POST.get("topic_id")
        user_id = request.user.id
        is_like = 1
        like = Likes.objects.create(topic_id=topic_id, user_id=user_id, is_like=is_like)
        if like.id > 0:
            return Show.success("点赞成功")
        else:
            return Show.fail("网络异常")
    else:
        return Show.fail("请求方法异常")


def hate(request):
    if request.method == "POST":
        topic_id = request.POST.get("topic_id")
        user_id = request.user.id
        is_like = 0
        like = Likes.objects.create(topic_id=topic_id, user_id=user_id, is_like=is_like)
        if like.id > 0:
            return Show.success("点赞成功")
        else:
            return Show.fail("网络异常")
    else:
        return Show.fail("请求方法异常")
