from django.shortcuts import render
from django.views import View

from bbs.models import Topics


class TopicView(View):

    def get(self, request, topic_id):
        topic = Topics.objects.get(id=topic_id)
        print(topic.user.username)
        return render(request, 'topics/show.html', locals())
