from django.urls import path

from bbs.comments import comments
from bbs.users import users_view
from bbs.blogs import my_blogs
from bbs.blogs import category
from bbs.blogs import topics

urlpatterns = [
    # 个人中心
    path('user_center/', users_view.UserCenter.as_view(), name='user_center'),
    path('users/settings/edit/', users_view.UserProfile.as_view(), name='edit_profile'),
    path('users/settings/update/', users_view.UserProfile.post, name='upload_profile'),
    path('users/settings/edit_avatar/', users_view.UserAvatar.as_view(), name='edit_avatar'),
    path('users/settings/edit_phone/', users_view.UserBindPhone.as_view(), name='edit_phone'),
    path('users/settings/edit_password/', users_view.UserChangePassword.as_view(), name='edit_password'),
    path('categories/<int:category_id>/', category.CategoryView.as_view(), name='category_show'),
    path('topics/<int:topic_id>/', topics.TopicView.as_view(), name='topic_show'),
    path('topics/edit/<int:topic_id>/', topics.UpdateTopicView.as_view(), name="edit_topic"),
    path('topics/update/', topics.UpdateTopicView.as_view(), name="update_topic"),
    path('topics/delete/', topics.DeleteTopicView.as_view(), name="delete_topic"),

    # 我的博客
    path('blog/<str:username>/', my_blogs.MyBlog.as_view(), name='blog_center'),
    # 新建博文
    path('topic/create/', my_blogs.CreateTopic.as_view(), name='create_topic'),
    # 点赞踩
    path('like/', my_blogs.like, name='like'),
    path('hate/', my_blogs.hate, name='hate'),
    path('comment/', comments.Comment.as_view(), name='commit'),
]
