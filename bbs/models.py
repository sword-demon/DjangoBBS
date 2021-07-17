# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import os
import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField

from .storage import ImageStorage


class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name='分类名称')
    description = models.TextField(blank=True, null=True, verbose_name='分类描述')
    post_count = models.PositiveIntegerField(verbose_name='帖子个数', default=0)
    create_time = models.IntegerField(verbose_name='创建时间')
    update_time = models.IntegerField(blank=True, null=True, verbose_name='更新时间')

    class Meta:
        db_table = 'categories'
        verbose_name = '帖子分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Comments(models.Model):
    pid = models.PositiveIntegerField(default=0)
    content = models.TextField()
    topic = models.ForeignKey(to="Topics", to_field="id", on_delete=models.CASCADE)
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'
        verbose_name = '评论表'
        verbose_name_plural = verbose_name


class Notifications(models.Model):
    title = models.CharField(max_length=191)
    content = models.TextField(blank=True, null=True)
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    is_read = models.PositiveIntegerField(default=0)
    create_time = models.IntegerField()
    update_time = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = '通知表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=50)
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    topic = models.ForeignKey(to="Topics", to_field="id", on_delete=models.CASCADE)

    class Meta:
        db_table = 'tags'
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Topics(models.Model):
    title = models.CharField(max_length=64)
    body = RichTextUploadingField(blank=True, null=True)
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    category = models.ForeignKey(to="Categories", to_field="id", on_delete=models.CASCADE)
    reply_count = models.PositiveIntegerField(default=0)
    view_count = models.PositiveIntegerField(default=0)
    sort = models.PositiveIntegerField(default=0)
    create_time = models.PositiveIntegerField()
    update_time = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'topics'
        verbose_name = '帖子表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Collects(models.Model):
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    topic = models.ForeignKey(to="Topics", to_field="id", on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=50, verbose_name='收藏的帖子标题')

    class Meta:
        db_table = "collects"
        verbose_name = '收藏表'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'topic'),)


class Likes(models.Model):
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    topic = models.ForeignKey(to="Topics", to_field="id", on_delete=models.CASCADE)
    is_like = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'likes'
        verbose_name = '点赞表'
        verbose_name_plural = verbose_name
        unique_together = (('user', 'topic'),)


class Users(AbstractUser):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    avatar = models.FileField(upload_to="avatar/%Y%m", default="/avatars/avatar.jpg", storage=ImageStorage())
    last_login_ip = models.CharField(max_length=64)
    update_time = models.IntegerField(blank=True, null=True)
    sex = models.PositiveIntegerField(default=0)
    email = models.CharField(max_length=64)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    birthday = models.DateTimeField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    github = models.CharField(max_length=255, blank=True, null=True)
    qq = models.CharField(max_length=12, blank=True, null=True)
    sign = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'


class Log(models.Model):
    user = models.ForeignKey(to="Users", to_field="id", on_delete=models.CASCADE)
    level = models.CharField(max_length=32, verbose_name='异常级别', default='info')
    request_path = models.CharField(max_length=191, verbose_name='请求地址')
    ip = models.CharField(max_length=64)
    params = models.TextField(verbose_name='请求参数')
    content = models.TextField(verbose_name='异常内容', null=True, blank=True)
    create_time = models.PositiveIntegerField()

    class Meta:
        db_table = 'logs'
        verbose_name = '日志记录表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.level
