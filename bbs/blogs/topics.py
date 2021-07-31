import time

from django.db import transaction
from django.http import QueryDict
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView

from bbs.forms.topic_form import CreateTopicForm
from bbs.models import Topics, Tags, Categories, Comments, Users
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
        replies = Comments.objects.filter(topic_id=topic_id).all()
        comment_list = self.build_msg(replies)

        comment_tree = self.build_comment_tree(topic)
        # print(comment_tree, type(comment_tree))

        return render(request, 'topics/show.html',
                      {"topic": topic, "tags": tags, "replies": replies, 'comments': comment_tree})

    def insert_comment_node(self, com_tree, comment):
        for parent, v in com_tree.items():
            if parent == comment.pid:
                # print("find %s's parent %s" % (comment.user.username, parent))
                com_tree[parent][comment] = {}
            else:
                # print("haven't found %s's parent, start looking into further layer..." % comment)
                self.insert_comment_node(com_tree[parent], comment)

    def build_comment_tree(self, topic_obj):
        all_comments = topic_obj.comments_set.select_related().order_by('id')
        # print(all_comments)
        comment_tree = {}
        for comment in all_comments:
            if comment.pid is None:
                # print("pid is None", comment)
                comment_tree[comment] = {}
            else:
                # print("pid is not None", comment_tree, comment)
                self.insert_comment_node(comment_tree, comment)

        # for k, v in comment_tree.items():
        #     print(k, v)

        return comment_tree

    def get_comment_list(self, comment_list):
        # 把msg增加一个children键值对，存放它的儿子们
        ret = []
        comment_dic = {}
        for comment_obj in comment_list:
            comment_obj['children'] = []
            comment_dic[comment_obj['pk']] = comment_obj

        for comment in comment_list:
            p_obj = comment_dic.get(comment['pid'])
            if not p_obj:
                ret.append(comment)
            else:
                p_obj['children'].append(comment)
        return ret

    def build_msg(self, comment_obj):
        """
        把数据造成列表里边套字典的形式
        :param comment_obj:
        :return:
        """
        msg = []
        for comment in comment_obj:
            data = {}
            if comment.pid:
                data['pid'] = comment.pid.id
                data['username'] = Comments.objects.get(pk=comment.pid.id).user.username
            else:
                data['pid'] = None
                data['username'] = None

            data['pk'] = comment.pk
            data['content'] = comment.content
            data['username'] = comment.user.username
            msg.append(data)
        return msg


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
