from django import forms
from django.core.exceptions import ValidationError

from bbs.models import Topics


class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topics
        fields = ['title', 'body', 'category']
        labels = {
                     "title": "文章标题",
                     "body": "文章内容"
                 },
        widgets = {
            "category": forms.Select(attrs={'class': "form-control col-sm-4"}),
            "title": forms.widgets.TextInput(attrs={"class": "form-control col-sm-7 ml-2", "placeholder": "标题"}),
        }

    def clean_body(self):
        val = self.cleaned_data.get("body")
        if val:
            return self.cleaned_data
        raise ValidationError("提交内容不能为空")
