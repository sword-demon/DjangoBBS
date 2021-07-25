from django import forms
from django.core.exceptions import ValidationError

from bbs.models import Topics


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ['title', 'body', 'category']
        exclude = ['user', 'create_time', 'update_time']
        labels = {
                     "title": "文章标题",
                     "body": "文章内容"
                 },
        widgets = {
            "category": forms.Select(attrs={'class': "form-control col-sm-4"}),
            "title": forms.widgets.TextInput(
                attrs={"class": "form-control col-sm-6 ml-2", "placeholder": "标题"}),
        }
        error_messages = {
            "category": {
                "required": "请选择分类"
            },
            "title": {"required": "文章标题不能为空", }
        }
