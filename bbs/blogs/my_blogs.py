import time

from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
# from ratelimit.decorators import ratelimit

from bbs.forms.topic_form import CreateTopicForm
from bbs.models import Topics, Users, Tags, Likes, Comments, Collects
from djangoBBS import dev, settings
from utils.decorator import check_login
from utils.json_response import Show


# from utils.mixin import LoginRequiredMixin


class MyBlog(View):

    def string_to_timestamp(self, str_date):
        time_array = time.strptime(str_date, "%Y-%m")
        time_stamp = int(float(time.mktime(time_array)))
        print(time_stamp)
        return time_stamp

    @method_decorator(check_login, name='get')
    def get(self, request, username, slug=None):
        """
        我的博文
        :param request:
        :param username: 用户名
        :param slug: 日期参数，查询归档
        :return:
        """
        if slug:
            # search_date = self.string_to_timestamp(slug)
            topics = Topics.objects.filter(user__username=username).extra(where=
            [
                "DATE_FORMAT(FROM_UNIXTIME(create_time), '%%Y-%%m')='" + slug + "'"])
            # print(request.path)
        else:
            # 根据用户名查询该用户的一些数据
            topics = Topics.objects.filter(user__username=username).all()
        for topic in topics:
            topic.like_num = Likes.objects.filter(topic_id=topic.id, is_like=1).count()  # 文章点赞数
            topic.hate_num = Likes.objects.filter(topic_id=topic.id, is_like=0).count()  # 文章踩数
            topic.comment_num = Comments.objects.filter(topic_id=topic.id).count()  # 文章评论数
        bloger = Users.objects.filter(username=username).first()  # 当前博客主
        likes = Likes.objects.filter(topic_id__in=topics.values("id"), is_like=1).count()  # 获取当前用户的所有的点赞数
        collects = Collects.objects.filter(user_id=bloger.id).count()  # 获取用户所有的收藏数(todo:点击收藏暂时没写)
        tags = Tags.objects.filter(user_id=bloger.id).values("title").annotate(c=Count("id")).values("c",
                                                                                                     "title")  # 获取当前查询的用户的所有的标签信息

        # 查询出的所有文章的按照年月归档
        date_list = Topics.objects.filter(user__username=username).extra(
            select={"y_m_date": "DATE_FORMAT(FROM_UNIXTIME(create_time),'%%Y-%%m')"}).values(
            "y_m_date").annotate(c=Count("id")).values("y_m_date", "c")
        # 不适合时间戳
        # date_list = Topics.objects.filter(user__username=username).annotate(month=TruncMonth('create_time')).values(
        #     "month").annotate(c=Count('id')).values("month", "c")
        # print(date_list)
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


@check_login
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


@check_login
def hate(request):
    if request.method == "POST":
        topic_id = request.POST.get("topic_id")
        user_id = request.user.id
        is_like = 0
        like = Likes.objects.create(topic_id=topic_id, user_id=user_id, is_like=is_like)
        if like.id > 0:
            return Show.success("踩成功")
        else:
            return Show.fail("网络异常")
    else:
        return Show.fail("请求方法异常")
