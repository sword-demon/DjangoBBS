from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView

from bbs.models import Topics, Tags, Categories
from utils.json_response import Show


class TopicView(View):

    def get(self, request, topic_id):
        topic = Topics.objects.get(id=topic_id)
        return render(request, 'topics/show.html', locals())


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
        pass


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
