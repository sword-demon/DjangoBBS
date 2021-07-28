from django.views import View

from bbs.models import Comments
from utils.json_response import Show


class Comment(View):
    def post(self, request):
        pid = request.POST.get("pid", None)
        print(pid)
        topic_id = request.POST.get("topic_id")
        if not topic_id:
            return Show.fail("参数缺失")
        content = request.POST.get("content", "")
        if not content:
            return Show.fail("请填写评论内容")
        comment_obj = Comments.objects.create(topic_id=int(topic_id), user_id=request.user.id, content=content,
                                              pid_id=pid)
        if comment_obj:
            return Show.success("提交成功")
        return Show.fail("提交失败")
