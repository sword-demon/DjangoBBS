import time

from django.db import transaction
from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView

from bbs.forms.topic_form import CreateTopicForm
from bbs.models import Topics, Tags, Categories, Comments
from utils.json_response import Show
from utils.tools import tree_list


class TopicView(View):
    """
    文章详情，后续可以使用DetailView
    """

    def get(self, request, topic_id):
        topic = Topics.objects.get(id=topic_id)
        # 获取tags
        tags = Tags.objects.filter(topic_id=topic_id).all()
        # 少用local
        replies = Comments.objects.filter(topic_id=topic_id).values()
        comments_list = tree_list(list(replies))
        print(comments_list)
        return render(request, 'topics/show.html',
                      {"topic": topic, "tags": tags, "replies": replies, 'comments': comments_list})


class UpdateTopicView(View):

    def get(self, request, topic_id):
        topic = Topics.objects.filter(id=topic_id).first()
        topic.tags = Tags.objects.filter(topic_id=topic_id, user_id=topic.user_id).values("title")
        categories = Categories.objects.all()
        tags_value = ""
        if topic.tags:
            for item in list(topic.tags):
                tags_value += item["title"] + ","
        return render(request, 'topics/edit.html', {"topic": topic, "tags_value": tags_value, "categories": categories})

    def post(self, request):
        topic_id = request.POST.get("id", 0)
        if not topic_id:
            return Show.fail("参数缺失")
        obj = Topics.objects.filter(id=topic_id).first()
        if not obj:
            return Show.fail("该文章已不存在")
        form = CreateTopicForm(data=request.POST, instance=obj)
        tags = request.POST.get("tags")
        tags_list = tags.split(",")
        if form.is_valid():
            with transaction.atomic():
                record = form.save(commit=False)
                record.user = request.user
                record.update_time = time.time()
                record.save()

                if tags:
                    # 先删除原先的标签信息，再进行重新添加
                    Tags.objects.filter(user_id=request.user.id, topic_id=topic_id).delete()
                    tags_insert_batch = []
                    for i in tags_list:
                        tags_insert_batch.append(Tags(title=i, user_id=request.user.id, topic_id=topic_id))

                    Tags.objects.bulk_create(tags_insert_batch)

            return Show.success("修改成功")
        else:
            return Show.fail(form.errors)


class DeleteTopicView(DeleteView):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(DeleteTopicView, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        DELETE = QueryDict(request.body)
        topic_id = DELETE.get("topic_id", 0)
        if not topic_id:
            return Show.fail("文章id参数缺失")

        Topics.objects.filter(id=int(topic_id)).delete()
        return Show.success("删除成功")
