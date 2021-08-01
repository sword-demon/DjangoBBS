from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View

from bbs.models import Comments
from utils.decorator import check_login
from utils.json_response import Show


class Comment(View):

    def get(self, request):
        """
        ajax加载评论内容
        :param request:
        :return:
        """
        topic_id = request.GET.get("topic_id")
        if not topic_id:
            pass
        data = list(Comments.objects.filter(topic_id=topic_id).values('pk', 'content', 'user_id', 'user__username',
                                                                      'user__avatar', 'pid_id', 'level').order_by('id'))
        # print(data, type(data))
        for item in data:
            item['parent_username'] = self.get_parent_username(item['pid_id'])

        return JsonResponse(data, safe=False)

    def get_parent_username(self, pid):
        """
        拼凑字段，获取父级评论用户的名称
        :param pid:
        :return:
        """
        if pid:
            return Comments.objects.filter(id=pid).first().user.username
        else:
            return ''

    def get_parent_level(self, pid):
        return Comments.objects.filter(id=pid).first().level

    @method_decorator(check_login, name='post')
    def post(self, request):
        pid = request.POST.get("pid", None)
        level = request.POST.get("level", None)
        if pid:
            # 根据评论的pid查询上一级的level，如果为空就默认填入 pid， 不为空则继续拼接_加这次提交的pid
            p_level = self.get_parent_level(pid)
            if p_level:
                level_path = p_level.split("_")
                level_path.append(level)
                level = "_".join(level_path)
        topic_id = request.POST.get("topic_id")
        if not topic_id:
            return Show.fail("参数缺失")
        content = request.POST.get("content", "")
        if not content:
            return Show.fail("请填写评论内容")
        comment_obj = Comments.objects.create(topic_id=int(topic_id), user_id=request.user.id, content=content,
                                              pid_id=pid, level=level)
        if comment_obj:
            return Show.success("提交成功")
        return Show.fail("提交失败")
