# Django 开发 BBS + Blog

## github地址
https://github.com/sword-demon/djangoBBS

## 构建项目

```bash
django-admin startproject djangoBBS
```

## 导出当前项目需要的类库

```bash
# 安装
pip install pipreqs  # 或者 pip3 install pipreqs

# 使用
pipreqs .  # . 表示当前目录

# 使用建议，导出前先定位到当前项目根目录
pipreqs ./ --encoding=utf8 # 该命令避免编码错误
```

## 日志以及全局记录中间件

> 设计了一个记录全局异常的日志表，使用中间件进行记录，在开发环境时直接提示错误内容，在生成环境下，提示固定内容。

## 文章阅读量中间件

根据请求的地址反向获取url的别名来判断是否是访问了文章详情页。

获取url的别名

```python
def process_request(self, request):
    from django.urls import resolve
    path = request.path
    rm = resolve(path)
    url_name = rm.url_name
    print(url_name)
```

就可以获取urls.py里给path设置的`name`属性的值。

## ImageStorage

> 重写Django的文件存储`save`方法，防止同一时间里并发上传文件时文件名重复的问题。
>

## 模板继承

使用了模板继承，将公共部分的页面进行分离。 对很多冗长的页面，使用`include`进行加载，进行分割页面代码。做到短小简练。

## JS封装了request请求方法

在全局异常处理的中间件里，我返回的内容是`json`格式的提示语， 所以，我直接写一个基本所有页面使用的`ajax`提交的信息回调函数处理格式。

```javascript
function request(url, option = {}, redirect_uri = "") {
    $.ajax({
        url,
        ...option,
        success: function (res) {
            if (res.status === 1) {
                layer.msg(res.msg, {
                    icon: 6
                }, function () {
                    if (redirect_uri != "") {
                        window.location.href = redirect_uri;
                    } else {
                        window.location.reload();
                    }
                });
            } else if (res.status === 2) {
                layer.msg(res.msg, {icon: 5}, function () {
                    window.location.href = "{% url 'login' %}";
                });
            } else {
                var result;
                if (typeof res.msg == "string") {
                    result = res.msg;
                } else {
                    var str = "";
                    $.each(res.msg, function (index, item) {
                        str += "<br>" + item[0]
                    });
                    result = str;
                }
                layer.msg(result, {
                    icon: 5,
                    time: 2000
                }, function () {
                    window.location.reload();
                });
            }
        },
        error: function () {
            layer.msg("系统网络异常");
            return false;
        },
    });
}
```
>这里使用了`layui`的弹窗插件来让页面提示更加优美。

## 封装固定的返回json格式
```python
from django.http import JsonResponse


class HttpStatusCode(object):
    SUCCESS = 1
    FAIL = 0


class Show(HttpStatusCode):

    @staticmethod
    def success(message='OK', data=None):
        result = {
            "status": HttpStatusCode.SUCCESS,
            "msg": message,
            "data": data
        }

        return JsonResponse(result)

    @staticmethod
    def fail(message='error', data=None, status=HttpStatusCode.FAIL):
        result = {
            "status": status,
            "msg": message,
            "data": data
        }

        return JsonResponse(result)

```

## 时间戳查询
```sql
select * from topics where date_format(FROM_UNIXTIME(create_time), '%Y-%m')='2021-07';
```
>值得注意的是，这里的如果放到django里
> 

```python
topics = Topics.objects.filter(user__username=username).extra(where=
            [
                "DATE_FORMAT(FROM_UNIXTIME(create_time), '%%Y-%%m')='" + slug + "'"])
```
格式化日期的地方需要加2个`%`

## 评论树
这里采用的是`window.onload`的方式再配合`ajax`获取数据进行页面渲染。
因此，我特地加了一个`level`字段来记录一下等级的深度。

```text
1
1_2
1_2_3
```

这样的格式。
在`js`进行判断层级超过2或等于2时，都`append`到当前的最高的父级下。不过就是加了点区别，下面都有`@`谁来表示你是回复的谁。


## 后续添加
我还设计了一个收藏表，暂时没有加上这个功能，后续有时间加上。。。

## SQL
```sql
/*
 Navicat Premium Data Transfer

 Source Server         : localhost-mysql5.7
 Source Server Type    : MySQL
 Source Server Version : 50732
 Source Host           : localhost:3306
 Source Schema         : django_bbs

 Target Server Type    : MySQL
 Target Server Version : 50732
 File Encoding         : 65001

 Date: 01/08/2021 23:51:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=57 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (5, 'Can add permission', 2, 'add_permission');
INSERT INTO `auth_permission` VALUES (6, 'Can change permission', 2, 'change_permission');
INSERT INTO `auth_permission` VALUES (7, 'Can delete permission', 2, 'delete_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can view permission', 2, 'view_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can add group', 3, 'add_group');
INSERT INTO `auth_permission` VALUES (10, 'Can change group', 3, 'change_group');
INSERT INTO `auth_permission` VALUES (11, 'Can delete group', 3, 'delete_group');
INSERT INTO `auth_permission` VALUES (12, 'Can view group', 3, 'view_group');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add 用户表', 6, 'add_users');
INSERT INTO `auth_permission` VALUES (22, 'Can change 用户表', 6, 'change_users');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 用户表', 6, 'delete_users');
INSERT INTO `auth_permission` VALUES (24, 'Can view 用户表', 6, 'view_users');
INSERT INTO `auth_permission` VALUES (25, 'Can add 帖子分类表', 7, 'add_categories');
INSERT INTO `auth_permission` VALUES (26, 'Can change 帖子分类表', 7, 'change_categories');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 帖子分类表', 7, 'delete_categories');
INSERT INTO `auth_permission` VALUES (28, 'Can view 帖子分类表', 7, 'view_categories');
INSERT INTO `auth_permission` VALUES (29, 'Can add 帖子表', 8, 'add_topics');
INSERT INTO `auth_permission` VALUES (30, 'Can change 帖子表', 8, 'change_topics');
INSERT INTO `auth_permission` VALUES (31, 'Can delete 帖子表', 8, 'delete_topics');
INSERT INTO `auth_permission` VALUES (32, 'Can view 帖子表', 8, 'view_topics');
INSERT INTO `auth_permission` VALUES (33, 'Can add 标签表', 9, 'add_tags');
INSERT INTO `auth_permission` VALUES (34, 'Can change 标签表', 9, 'change_tags');
INSERT INTO `auth_permission` VALUES (35, 'Can delete 标签表', 9, 'delete_tags');
INSERT INTO `auth_permission` VALUES (36, 'Can view 标签表', 9, 'view_tags');
INSERT INTO `auth_permission` VALUES (37, 'Can add 通知表', 10, 'add_notifications');
INSERT INTO `auth_permission` VALUES (38, 'Can change 通知表', 10, 'change_notifications');
INSERT INTO `auth_permission` VALUES (39, 'Can delete 通知表', 10, 'delete_notifications');
INSERT INTO `auth_permission` VALUES (40, 'Can view 通知表', 10, 'view_notifications');
INSERT INTO `auth_permission` VALUES (41, 'Can add 评论表', 11, 'add_comments');
INSERT INTO `auth_permission` VALUES (42, 'Can change 评论表', 11, 'change_comments');
INSERT INTO `auth_permission` VALUES (43, 'Can delete 评论表', 11, 'delete_comments');
INSERT INTO `auth_permission` VALUES (44, 'Can view 评论表', 11, 'view_comments');
INSERT INTO `auth_permission` VALUES (45, 'Can add 点赞表', 12, 'add_likes');
INSERT INTO `auth_permission` VALUES (46, 'Can change 点赞表', 12, 'change_likes');
INSERT INTO `auth_permission` VALUES (47, 'Can delete 点赞表', 12, 'delete_likes');
INSERT INTO `auth_permission` VALUES (48, 'Can view 点赞表', 12, 'view_likes');
INSERT INTO `auth_permission` VALUES (49, 'Can add 收藏表', 13, 'add_collects');
INSERT INTO `auth_permission` VALUES (50, 'Can change 收藏表', 13, 'change_collects');
INSERT INTO `auth_permission` VALUES (51, 'Can delete 收藏表', 13, 'delete_collects');
INSERT INTO `auth_permission` VALUES (52, 'Can view 收藏表', 13, 'view_collects');
INSERT INTO `auth_permission` VALUES (53, 'Can add 日志记录表', 14, 'add_log');
INSERT INTO `auth_permission` VALUES (54, 'Can change 日志记录表', 14, 'change_log');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 日志记录表', 14, 'delete_log');
INSERT INTO `auth_permission` VALUES (56, 'Can view 日志记录表', 14, 'view_log');
COMMIT;

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `post_count` int(10) unsigned NOT NULL,
  `create_time` int(11) NOT NULL,
  `update_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of categories
-- ----------------------------
BEGIN;
INSERT INTO `categories` VALUES (1, '分享', '文章', 0, 1626538648, NULL);
INSERT INTO `categories` VALUES (2, '教程', '开发技巧、推荐扩展包等', 0, 1626790899, NULL);
INSERT INTO `categories` VALUES (3, '问答', '请保持友善，互帮互助', 0, 1626790952, NULL);
INSERT INTO `categories` VALUES (4, '公告', '站点公告', 0, 1626790952, NULL);
COMMIT;

-- ----------------------------
-- Table structure for collects
-- ----------------------------
DROP TABLE IF EXISTS `collects`;
CREATE TABLE `collects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic_name` varchar(50) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `collects_user_id_topic_id_370942b3_uniq` (`user_id`,`topic_id`),
  KEY `collects_topic_id_8607b607_fk_topics_id` (`topic_id`),
  CONSTRAINT `collects_topic_id_8607b607_fk_topics_id` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`),
  CONSTRAINT `collects_user_id_d554ce05_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of collects
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` longtext NOT NULL,
  `pid_id` int(11) DEFAULT NULL,
  `topic_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `level` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_pid_id_90532db8_fk_comments_id` (`pid_id`),
  KEY `comments_topic_id_f08e5362_fk_topics_id` (`topic_id`),
  KEY `comments_user_id_b8fd0b64_fk_users_id` (`user_id`),
  CONSTRAINT `comments_pid_id_90532db8_fk_comments_id` FOREIGN KEY (`pid_id`) REFERENCES `comments` (`id`),
  CONSTRAINT `comments_topic_id_f08e5362_fk_topics_id` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`),
  CONSTRAINT `comments_user_id_b8fd0b64_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of comments
-- ----------------------------
BEGIN;
INSERT INTO `comments` VALUES (1, 'lihiale', NULL, 5, 2, '');
INSERT INTO `comments` VALUES (2, '66666', 1, 5, 2, '1');
INSERT INTO `comments` VALUES (3, '我确实牛逼', 2, 5, 1, '1_2');
INSERT INTO `comments` VALUES (4, '...。。。', NULL, 5, 2, '');
INSERT INTO `comments` VALUES (5, 'dwqdwqq', NULL, 4, 2, '');
INSERT INTO `comments` VALUES (6, '无解', NULL, 4, 1, '');
INSERT INTO `comments` VALUES (7, '给wujie的评论', 6, 4, 1, '6');
INSERT INTO `comments` VALUES (8, '给wxvirus的评论', 5, 4, 1, '5');
INSERT INTO `comments` VALUES (9, '第三级别评论', 7, 4, 1, '6_7');
INSERT INTO `comments` VALUES (10, '第四级评论', 9, 4, 1, '6_7_9');
COMMIT;

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (7, 'bbs', 'categories');
INSERT INTO `django_content_type` VALUES (13, 'bbs', 'collects');
INSERT INTO `django_content_type` VALUES (11, 'bbs', 'comments');
INSERT INTO `django_content_type` VALUES (12, 'bbs', 'likes');
INSERT INTO `django_content_type` VALUES (14, 'bbs', 'log');
INSERT INTO `django_content_type` VALUES (10, 'bbs', 'notifications');
INSERT INTO `django_content_type` VALUES (9, 'bbs', 'tags');
INSERT INTO `django_content_type` VALUES (8, 'bbs', 'topics');
INSERT INTO `django_content_type` VALUES (6, 'bbs', 'users');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2021-07-13 20:05:29.456544');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2021-07-13 20:05:29.527571');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2021-07-13 20:05:29.621915');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2021-07-13 20:05:29.793084');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2021-07-13 20:05:29.798438');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2021-07-13 20:05:29.803271');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2021-07-13 20:05:29.807531');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2021-07-13 20:05:29.808747');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2021-07-13 20:05:29.813172');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2021-07-13 20:05:29.817816');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2021-07-13 20:05:29.822357');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2021-07-13 20:05:29.847454');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2021-07-13 20:05:29.852478');
INSERT INTO `django_migrations` VALUES (14, 'bbs', '0001_initial', '2021-07-13 20:05:30.286463');
INSERT INTO `django_migrations` VALUES (15, 'admin', '0001_initial', '2021-07-13 20:05:30.930668');
INSERT INTO `django_migrations` VALUES (16, 'admin', '0002_logentry_remove_auto_add', '2021-07-13 20:05:31.010336');
INSERT INTO `django_migrations` VALUES (17, 'admin', '0003_logentry_add_action_flag_choices', '2021-07-13 20:05:31.020761');
INSERT INTO `django_migrations` VALUES (18, 'bbs', '0002_auto_20210713_1103', '2021-07-13 20:05:31.053624');
INSERT INTO `django_migrations` VALUES (19, 'bbs', '0003_log', '2021-07-13 20:05:31.077254');
INSERT INTO `django_migrations` VALUES (20, 'bbs', '0004_auto_20210713_1118', '2021-07-13 20:05:31.208694');
INSERT INTO `django_migrations` VALUES (21, 'bbs', '0005_users_sign', '2021-07-13 20:05:31.247952');
INSERT INTO `django_migrations` VALUES (22, 'sessions', '0001_initial', '2021-07-13 20:05:31.279088');
INSERT INTO `django_migrations` VALUES (23, 'bbs', '0006_auto_20210714_1936', '2021-07-14 19:36:13.224043');
INSERT INTO `django_migrations` VALUES (24, 'bbs', '0007_auto_20210714_2237', '2021-07-14 22:37:35.538701');
INSERT INTO `django_migrations` VALUES (25, 'bbs', '0008_auto_20210715_1032', '2021-07-22 22:03:17.165643');
INSERT INTO `django_migrations` VALUES (26, 'bbs', '0009_auto_20210717_1019', '2021-07-22 22:03:17.173497');
INSERT INTO `django_migrations` VALUES (27, 'bbs', '0010_auto_20210722_2203', '2021-07-22 22:03:17.239516');
INSERT INTO `django_migrations` VALUES (28, 'bbs', '0002_comments', '2021-07-27 00:57:49.192799');
INSERT INTO `django_migrations` VALUES (29, 'bbs', '0003_comments_level', '2021-08-01 16:01:31.811265');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('8qw8i3l8lcgxvueol6hk8ap168u08mli', 'Nzk5ZWU0NGZiOWY4YzdkNWE0MTFjNGQ2M2VlODM1ZDBhYTlkY2ZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzY3N2MzOTMyZDA3MzQ4MzVlOGQ5NmE3OTM0NThjMzY4MzMzNjAwIn0=', '2021-08-15 23:11:29.338465');
INSERT INTO `django_session` VALUES ('fhrsvuhqtgx9pcluqvm7nahyhl48j1ll', 'Nzk5ZWU0NGZiOWY4YzdkNWE0MTFjNGQ2M2VlODM1ZDBhYTlkY2ZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzY3N2MzOTMyZDA3MzQ4MzVlOGQ5NmE3OTM0NThjMzY4MzMzNjAwIn0=', '2021-08-05 22:44:49.867738');
INSERT INTO `django_session` VALUES ('gtpwv7wncq3rtj0ay8v0hrr4ow91wf8q', 'Mzg1NGM4NzIzZDRhODA2M2IzZmUxM2Y5NzEzOTg0OTczNWIxYTJkMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0ODYyZWJjMDY2MmVkYjQ0OTg0YTJkNTliNTVmMTAwYTc3M2MwODE1In0=', '2021-08-08 22:57:12.825795');
INSERT INTO `django_session` VALUES ('st4xed157irvg5jpe8lj0graa433szv4', 'Nzk5ZWU0NGZiOWY4YzdkNWE0MTFjNGQ2M2VlODM1ZDBhYTlkY2ZkNTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyMzY3N2MzOTMyZDA3MzQ4MzVlOGQ5NmE3OTM0NThjMzY4MzMzNjAwIn0=', '2021-08-15 17:04:24.611640');
COMMIT;

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `is_like` int(10) unsigned NOT NULL,
  `topic_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `likes_topic_id_9c01a4dc_fk_topics_id` (`topic_id`),
  KEY `likes_user_id_0899754c` (`user_id`),
  CONSTRAINT `likes_topic_id_9c01a4dc_fk_topics_id` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`),
  CONSTRAINT `likes_user_id_0899754c_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of likes
-- ----------------------------
BEGIN;
INSERT INTO `likes` VALUES (3, 1, 2, 1);
INSERT INTO `likes` VALUES (6, 1, 2, 1);
INSERT INTO `likes` VALUES (7, 1, 2, 1);
INSERT INTO `likes` VALUES (8, 1, 2, 1);
INSERT INTO `likes` VALUES (9, 0, 2, 1);
INSERT INTO `likes` VALUES (10, 0, 2, 1);
COMMIT;

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `request_path` varchar(191) NOT NULL,
  `ip` varchar(64) NOT NULL,
  `params` longtext NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` longtext,
  `level` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `logs_user_id_237f5f83_fk_users_id` (`user_id`),
  CONSTRAINT `logs_user_id_237f5f83_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of logs
-- ----------------------------
BEGIN;
INSERT INTO `logs` VALUES (1, '/bbs/topic/create/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"a3qGvvJ1jPfAAdCqWlpBmpKgg9jXJXV9xCLQSohL6Sd93cSJ4q4n05CYsv8zJeEz\", \"category\": \"1\", \"title\": \"\\u83dc\\u5355\", \"body\": \"\"}', 1626542663, 1, 'division by zero', 'error');
INSERT INTO `logs` VALUES (11, '/bbs/blog/wujie/', '127.0.0.1', '{}', 1626881438, 1, 'Cannot resolve keyword \'is_like\' into field. Choices are: id, title, topic, topic_id, user, user_id', 'error');
INSERT INTO `logs` VALUES (12, '/bbs/like', '127.0.0.1', '{\"topic_id\": \"2\", \"csrfmiddlewaretoken\": \"FYzUIzQDzZRv3TjQjJsOUIgWHNgyFami80PiAzpkHpDOzaiIsQpdGsksSg5HGK1L\"}', 1626962503, 1, '(1062, \"Duplicate entry \'1-2\' for key \'likes_user_id_topic_id_9a12616a_uniq\'\")', 'error');
INSERT INTO `logs` VALUES (13, '/bbs/like', '127.0.0.1', '{\"topic_id\": \"2\", \"csrfmiddlewaretoken\": \"cUiYaAHdtUyKz66LWcssaBivDP33FsDWFWym2AgUBkk35n5D5jpRWlm1OiScG2ip\"}', 1626962508, 1, '(1062, \"Duplicate entry \'1-2\' for key \'likes_user_id_topic_id_9a12616a_uniq\'\")', 'error');
INSERT INTO `logs` VALUES (14, '/bbs/blog/wujie/', '127.0.0.1', '{}', 1626963569, 1, 'Cannot use QuerySet for \"Topics\": Use a QuerySet for \"Likes\".', 'error');
INSERT INTO `logs` VALUES (15, '/bbs/topics/1/', '127.0.0.1', '{}', 1626969607, 1, 'Topics matching query does not exist.', 'error');
INSERT INTO `logs` VALUES (16, '/bbs/topics/edit/5/', '127.0.0.1', '{}', 1626970461, 1, '\'Topics\' object has no attribute \'query\'', 'error');
INSERT INTO `logs` VALUES (17, '/bbs/topics/edit/5/', '127.0.0.1', '{}', 1626970469, 1, '\'Topics\' object has no attribute \'query\'', 'error');
INSERT INTO `logs` VALUES (18, '/media/%7B%7B%20topic.user.avatar%20%7D%7D', '127.0.0.1', '{}', 1626971240, 1, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/{{ topic.user.avatar }}\" 不存在', 'error');
INSERT INTO `logs` VALUES (19, '/media/%7B%7B%20topic.user.avatar%20%7D%7D', '127.0.0.1', '{}', 1626971279, 1, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/{{ topic.user.avatar }}\" 不存在', 'error');
INSERT INTO `logs` VALUES (20, '/media/%7B%7B%20topic.user.avatar%20%7D%7D', '127.0.0.1', '{}', 1626971292, 1, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/{{ topic.user.avatar }}\" 不存在', 'error');
INSERT INTO `logs` VALUES (21, '/bbs/topics/update/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"Ac2ux1lICuRd95RyXLiC5vSC9ARa2WxYwMFUg2WJPwASqveRBFxoI6UycfDq0zBL\", \"category\": \"1\", \"title\": \"Django DeleteView \\u5220\\u9664\", \"body\": \"<pre>\\n{% extends &#39;layout/app.html&#39; %}\\n\\n{% block title %}\\n    \\u6587\\u7ae0\\u6807\\u9898\\n{% endblock %}\\n\\n{% block content %}\\n    &lt;div class=&quot;row&quot;&gt;\\n\\n        &lt;div class=&quot;col-lg-3 col-md-3 hidden-sm hidden-xs author-info&quot;&gt;\\n            &lt;div class=&quot;card &quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    &lt;div class=&quot;text-center&quot;&gt;\\n                        \\u4f5c\\u8005\\uff1a{{ topic.user.username }}\\n                    &lt;/div&gt;\\n                    &lt;hr&gt;\\n                    &lt;div class=&quot;media&quot;&gt;\\n                        &lt;div align=&quot;center&quot;&gt;\\n                            &lt;a href=&quot;&quot;&gt;\\n                                &lt;img class=&quot;thumbnail img-fluid&quot; src=&quot;/media/{{ topic.user.avatar }}&quot; width=&quot;300px&quot;\\n                                     height=&quot;300px&quot;&gt;\\n                            &lt;/a&gt;\\n                        &lt;/div&gt;\\n                    &lt;/div&gt;\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n        &lt;/div&gt;\\n\\n        &lt;div class=&quot;col-lg-9 col-md-9 col-sm-12 col-xs-12 topic-content&quot;&gt;\\n            &lt;div class=&quot;card&quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    &lt;h1 class=&quot;text-center mt-3 mb-3&quot;&gt;\\n                        {{ topic.title }}\\n                    &lt;/h1&gt;\\n\\n                    &lt;div class=&quot;article-meta text-center text-secondary&quot;&gt;\\n                        {% load mylabel %}\\n                        {{ topic.create_time|timestamp }}\\n                        &sdot;\\n                        &lt;i class=&quot;far fa-comment&quot;&gt;&lt;/i&gt;\\n                        {{ topic.reply_count }}\\n                    &lt;/div&gt;\\n\\n                    &lt;div class=&quot;topic-body mt-4 mb-4&quot;&gt;\\n                        {{ topic.body|safe }}\\n                    &lt;/div&gt;\\n\\n                    &lt;!-- \\u5224\\u65ad\\u662f\\u4e0d\\u662f\\u81ea\\u5df1\\u7684\\u6587\\u7ae0 --&gt;\\n                    {% if request.user.id == topic.user.id %}\\n                        &lt;div class=&quot;operate&quot;&gt;\\n                            &lt;hr&gt;\\n                            &lt;a href=&quot;{% url &#39;edit_topic&#39; topic.id %}&quot; class=&quot;btn btn-outline-secondary btn-sm&quot;\\n                               role=&quot;button&quot;&gt;\\n                                &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt; \\u7f16\\u8f91\\n                            &lt;/a&gt;\\n\\n                            &lt;button type=&quot;button&quot; data-topic_id=&quot;{{ topic.id }}&quot;\\n                                    class=&quot;btn_delete_topic btn btn-outline-secondary btn-sm&quot;&gt;\\n                                &lt;i class=&quot;fa fa-trash&quot;&gt;&lt;/i&gt; \\u5220\\u9664\\n                            &lt;/button&gt;\\n                        &lt;/div&gt;\\n                    {% endif %}\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n\\n            &lt;!-- \\u7528\\u6237\\u56de\\u590d\\u5217\\u8868 --&gt;\\n            &lt;div class=&quot;card topic-reply mt-4&quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    {% include &#39;topics/_reply_box.html&#39; %}\\n                    {#                    {% include &#39;topics/_reply_list.html&#39; %}#}\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n\\n        &lt;/div&gt;\\n    &lt;/div&gt;\\n{% endblock %}\\n\\n{% block js %}\\n    &lt;script&gt;\\n        $(document).on(&quot;click&quot;, &quot;.btn_delete_topic&quot;, function () {\\n            var topic_id = $(this).data(&quot;topic_id&quot;);\\n            if (!topic_id) {\\n                layer.msg(&quot;\\u6587\\u7ae0id\\u53c2\\u6570\\u7f3a\\u5931&quot;);\\n                return false;\\n            }\\n            layer.confirm(&quot;\\u4f60\\u786e\\u5b9a\\u8981\\u5220\\u9664\\u5417&quot;, {\\n                btn: [&#39;\\u786e\\u5b9a&#39;, &#39;\\u53d6\\u6d88&#39;],\\n                title: &quot;\\u63d0\\u793a&quot;\\n            }, function () {\\n                request(&quot;{% url &#39;delete_topic&#39; %}&quot;, {\\n                    data: {\\n                        &quot;topic_id&quot;: topic_id,\\n                        &quot;csrfmiddlewaretoken&quot;: &quot;{{ csrf_token }}&quot;,\\n                    },\\n                    type: &quot;DELETE&quot;,\\n                    dataType: &quot;json&quot;,\\n                }, &quot;{% url &#39;blog_center&#39; request.user.username %}&quot;);\\n            });\\n        });\\n    &lt;/script&gt;\\n{% endblock %}\\n\\n</pre>\\n\", \"tags\": \"Django,CBV\", \"id\": \"5\"}', 1627186388, 1, 'update() argument after ** must be a mapping, not list', 'error');
INSERT INTO `logs` VALUES (22, '/bbs/topics/update/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"vRW12m2NPKUlJqf4YMQd4gHGPdvuBeIErrzrLnDO2MD00QCnCG5ZHRJCSShKzRMr\", \"category\": \"1\", \"title\": \"Django DeleteView \\u5220\\u9664\", \"body\": \"<pre>\\n{% extends &#39;layout/app.html&#39; %}\\n\\n{% block title %}\\n    \\u6587\\u7ae0\\u6807\\u9898\\n{% endblock %}\\n\\n{% block content %}\\n    &lt;div class=&quot;row&quot;&gt;\\n\\n        &lt;div class=&quot;col-lg-3 col-md-3 hidden-sm hidden-xs author-info&quot;&gt;\\n            &lt;div class=&quot;card &quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    &lt;div class=&quot;text-center&quot;&gt;\\n                        \\u4f5c\\u8005\\uff1a{{ topic.user.username }}\\n                    &lt;/div&gt;\\n                    &lt;hr&gt;\\n                    &lt;div class=&quot;media&quot;&gt;\\n                        &lt;div align=&quot;center&quot;&gt;\\n                            &lt;a href=&quot;&quot;&gt;\\n                                &lt;img class=&quot;thumbnail img-fluid&quot; src=&quot;/media/{{ topic.user.avatar }}&quot; width=&quot;300px&quot;\\n                                     height=&quot;300px&quot;&gt;\\n                            &lt;/a&gt;\\n                        &lt;/div&gt;\\n                    &lt;/div&gt;\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n        &lt;/div&gt;\\n\\n        &lt;div class=&quot;col-lg-9 col-md-9 col-sm-12 col-xs-12 topic-content&quot;&gt;\\n            &lt;div class=&quot;card&quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    &lt;h1 class=&quot;text-center mt-3 mb-3&quot;&gt;\\n                        {{ topic.title }}\\n                    &lt;/h1&gt;\\n\\n                    &lt;div class=&quot;article-meta text-center text-secondary&quot;&gt;\\n                        {% load mylabel %}\\n                        {{ topic.create_time|timestamp }}\\n                        &sdot;\\n                        &lt;i class=&quot;far fa-comment&quot;&gt;&lt;/i&gt;\\n                        {{ topic.reply_count }}\\n                    &lt;/div&gt;\\n\\n                    &lt;div class=&quot;topic-body mt-4 mb-4&quot;&gt;\\n                        {{ topic.body|safe }}\\n                    &lt;/div&gt;\\n\\n                    &lt;!-- \\u5224\\u65ad\\u662f\\u4e0d\\u662f\\u81ea\\u5df1\\u7684\\u6587\\u7ae0 --&gt;\\n                    {% if request.user.id == topic.user.id %}\\n                        &lt;div class=&quot;operate&quot;&gt;\\n                            &lt;hr&gt;\\n                            &lt;a href=&quot;{% url &#39;edit_topic&#39; topic.id %}&quot; class=&quot;btn btn-outline-secondary btn-sm&quot;\\n                               role=&quot;button&quot;&gt;\\n                                &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt; \\u7f16\\u8f91\\n                            &lt;/a&gt;\\n\\n                            &lt;button type=&quot;button&quot; data-topic_id=&quot;{{ topic.id }}&quot;\\n                                    class=&quot;btn_delete_topic btn btn-outline-secondary btn-sm&quot;&gt;\\n                                &lt;i class=&quot;fa fa-trash&quot;&gt;&lt;/i&gt; \\u5220\\u9664\\n                            &lt;/button&gt;\\n                        &lt;/div&gt;\\n                    {% endif %}\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n\\n            &lt;!-- \\u7528\\u6237\\u56de\\u590d\\u5217\\u8868 --&gt;\\n            &lt;div class=&quot;card topic-reply mt-4&quot;&gt;\\n                &lt;div class=&quot;card-body&quot;&gt;\\n                    {% include &#39;topics/_reply_box.html&#39; %}\\n                    {#                    {% include &#39;topics/_reply_list.html&#39; %}#}\\n                &lt;/div&gt;\\n            &lt;/div&gt;\\n\\n        &lt;/div&gt;\\n    &lt;/div&gt;\\n{% endblock %}\\n\\n{% block js %}\\n    &lt;script&gt;\\n        $(document).on(&quot;click&quot;, &quot;.btn_delete_topic&quot;, function () {\\n            var topic_id = $(this).data(&quot;topic_id&quot;);\\n            if (!topic_id) {\\n                layer.msg(&quot;\\u6587\\u7ae0id\\u53c2\\u6570\\u7f3a\\u5931&quot;);\\n                return false;\\n            }\\n            layer.confirm(&quot;\\u4f60\\u786e\\u5b9a\\u8981\\u5220\\u9664\\u5417&quot;, {\\n                btn: [&#39;\\u786e\\u5b9a&#39;, &#39;\\u53d6\\u6d88&#39;],\\n                title: &quot;\\u63d0\\u793a&quot;\\n            }, function () {\\n                request(&quot;{% url &#39;delete_topic&#39; %}&quot;, {\\n                    data: {\\n                        &quot;topic_id&quot;: topic_id,\\n                        &quot;csrfmiddlewaretoken&quot;: &quot;{{ csrf_token }}&quot;,\\n                    },\\n                    type: &quot;DELETE&quot;,\\n                    dataType: &quot;json&quot;,\\n                }, &quot;{% url &#39;blog_center&#39; request.user.username %}&quot;);\\n            });\\n        });\\n    &lt;/script&gt;\\n{% endblock %}\\n\\n</pre>\\n\", \"tags\": \"Django,CBV\", \"id\": \"5\"}', 1627186488, 1, 'update() takes 1 positional argument but 3 were given', 'error');
INSERT INTO `logs` VALUES (37, '/bbs/comment/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"WQ4IV9aMUpTk7LzjONDeaRpfGPKzk4zhmi8E1j4CNDRo8T8lYnZF8Hb1xpR0QzNW\", \"topic_id\": \"5\", \"pid\": \"0\", \"content\": \"dwqdwq\"}', 1627320970, 2, 'The database backend does not accept 0 as a value for AutoField.', 'error');
INSERT INTO `logs` VALUES (38, '/media/', '127.0.0.1', '{}', 1627479700, 1, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (39, '/media/', '127.0.0.1', '{}', 1627479705, 1, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (40, '/media/', '127.0.0.1', '{}', 1627479709, 1, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (41, '/bbs/comment/', '127.0.0.1', '{\"pid\": \"1\", \"topic_id\": \"5\", \"csrfmiddlewaretoken\": \"2rajS0dIFyC5gfzBU2koizMPYhqAVUYZcKR5mtHIHWUGjowmzlARUW8NeGadfRJY\", \"content\": \"666\"}', 1627479722, 1, '(1048, \"Column \'user_id\' cannot be null\")', 'error');
INSERT INTO `logs` VALUES (42, '/media/', '127.0.0.1', '{}', 1627479724, 1, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (43, '/media/', '127.0.0.1', '{}', 1627479802, 1, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (44, '/media/', '127.0.0.1', '{}', 1627479893, 2, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (45, '/media/', '127.0.0.1', '{}', 1627479903, 2, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (46, '/media/', '127.0.0.1', '{}', 1627479926, 2, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (47, '/media/', '127.0.0.1', '{}', 1627479949, 2, '这里不允许目录索引', 'error');
INSERT INTO `logs` VALUES (48, '/bbs/topics/5/', '127.0.0.1', '{}', 1627479987, 2, '\'Comments\' object is not subscriptable', 'error');
INSERT INTO `logs` VALUES (49, '/bbs/topics/5/', '127.0.0.1', '{}', 1627480005, 2, '\'Comments\' object is not subscriptable', 'error');
INSERT INTO `logs` VALUES (50, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807024, 2, '__call__() missing 1 required keyword-only argument: \'manager\'', 'error');
INSERT INTO `logs` VALUES (51, '/media/undefined', '127.0.0.1', '{}', 1627807024, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (52, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807547, 2, '\'dict\' object has no attribute \'pid_id\'', 'error');
INSERT INTO `logs` VALUES (53, '/media/undefined', '127.0.0.1', '{}', 1627807547, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (54, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807586, 2, '\'pid\'', 'error');
INSERT INTO `logs` VALUES (55, '/media/undefined', '127.0.0.1', '{}', 1627807586, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (56, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807593, 2, 'Users matching query does not exist.', 'error');
INSERT INTO `logs` VALUES (57, '/media/undefined', '127.0.0.1', '{}', 1627807593, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (58, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807615, 2, 'Users matching query does not exist.', 'error');
INSERT INTO `logs` VALUES (59, '/media/undefined', '127.0.0.1', '{}', 1627807615, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (60, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807769, 2, 'Users matching query does not exist.', 'error');
INSERT INTO `logs` VALUES (61, '/media/undefined', '127.0.0.1', '{}', 1627807769, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (62, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807847, 2, '\'NoneType\' object has no attribute \'username\'', 'error');
INSERT INTO `logs` VALUES (63, '/media/undefined', '127.0.0.1', '{}', 1627807847, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (64, '/bbs/comment/?topic_id=5', '127.0.0.1', '{\"topic_id\": \"5\"}', 1627807903, 2, '\'NoneType\' object has no attribute \'username\'', 'error');
INSERT INTO `logs` VALUES (65, '/media/undefined', '127.0.0.1', '{}', 1627807903, 2, '\"/Users/wangxin/PycharmProjects/djangoBBS/media/undefined\" 不存在', 'error');
INSERT INTO `logs` VALUES (66, '/bbs/comment/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"PBVfvjTZNiFn45MHNpoXRo5Ckoc9lcXm0CbOiU55XwbWQF4hRJ0be1CciOwsw56T\", \"topic_id\": \"4\", \"pid\": \"7\", \"level\": \"7\", \"content\": \"\\u7b2c\\u4e09\\u7ea7\\u8bc4\\u8bba\"}', 1627811672, 1, '\'list\' object has no attribute \'join\'', 'error');
INSERT INTO `logs` VALUES (67, '/bbs/comment/', '127.0.0.1', '{\"csrfmiddlewaretoken\": \"gYFxwEbrAq47LS7YO7sqK8iFtt28S0H0rZV6jfnxKEAGxspySr4E7LPfrTmr3TQx\", \"topic_id\": \"4\", \"pid\": \"7\", \"level\": \"7\", \"content\": \"\\u7b2c\\u4e09\\u7ea7\\u8bc4\\u8bba\"}', 1627811752, 1, '\'list\' object has no attribute \'join\'', 'error');
INSERT INTO `logs` VALUES (68, '/bbs/blog/wujie/', '127.0.0.1', '{}', 1627813139, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (69, '/bbs/blog/wujie/', '127.0.0.1', '{}', 1627813257, 1, 'unsupported format character \'Y\' (0x59) at index 49', 'error');
INSERT INTO `logs` VALUES (70, '/bbs/blog/wujie/', '127.0.0.1', '{}', 1627814067, 1, '\'create_time\' isn\'t a DateField, TimeField, or DateTimeField.', 'error');
INSERT INTO `logs` VALUES (71, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627815813, 1, 'get() got an unexpected keyword argument \'slug\'', 'error');
INSERT INTO `logs` VALUES (72, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627815839, 1, 'get() got an unexpected keyword argument \'slug\'', 'error');
INSERT INTO `logs` VALUES (73, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627825815, 1, 'time data \'2021-07\' does not match format \'%Y-%m-%d %H:%M:%S\'', 'error');
INSERT INTO `logs` VALUES (74, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826225, 1, 'time data \'2021-07\' does not match format \'%Y-%m-%d %H:%M:%S\'', 'error');
INSERT INTO `logs` VALUES (75, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826227, 1, 'time data \'2021-07\' does not match format \'%Y-%m-%d %H:%M:%S\'', 'error');
INSERT INTO `logs` VALUES (76, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826229, 1, 'time data \'2021-07\' does not match format \'%Y-%m-%d %H:%M:%S\'', 'error');
INSERT INTO `logs` VALUES (77, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826245, 1, 'Tuple or struct_time argument required', 'error');
INSERT INTO `logs` VALUES (78, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826298, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (79, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826299, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (80, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826299, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (81, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826379, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (82, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826381, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (83, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826496, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (84, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826544, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (85, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826569, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (86, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826896, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (87, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627826907, 1, 'invalid literal for int() with base 10: \'2021-07\'', 'error');
INSERT INTO `logs` VALUES (88, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827423, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (89, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827424, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (90, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827426, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (91, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827468, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (92, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827470, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (93, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827471, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (94, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827471, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (95, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827471, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (96, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827471, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (97, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827472, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (98, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827472, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (99, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827472, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (100, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827479, 1, '(1305, \'FUNCTION django_bbs.DATEFORMAT does not exist\')', 'error');
INSERT INTO `logs` VALUES (101, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827505, 1, '(1305, \'FUNCTION django_bbs.FORM_UNIXTIME does not exist\')', 'error');
INSERT INTO `logs` VALUES (102, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827510, 1, '(1305, \'FUNCTION django_bbs.FORM_UNIXTIME does not exist\')', 'error');
INSERT INTO `logs` VALUES (103, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827510, 1, '(1305, \'FUNCTION django_bbs.FORM_UNIXTIME does not exist\')', 'error');
INSERT INTO `logs` VALUES (104, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827510, 1, '(1305, \'FUNCTION django_bbs.FORM_UNIXTIME does not exist\')', 'error');
INSERT INTO `logs` VALUES (105, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827546, 1, '(1305, \'FUNCTION django_bbs.FORM_UNIXTIME does not exist\')', 'error');
INSERT INTO `logs` VALUES (106, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827923, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (107, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627827936, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (108, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627828346, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (109, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627828348, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (110, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627828348, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (111, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627828348, 1, 'not enough arguments for format string', 'error');
INSERT INTO `logs` VALUES (112, '/bbs/blog/wujie/archive/2021-07', '127.0.0.1', '{}', 1627828695, 1, '\'WSGIRequest\' object has no attribute \'pathinfo\'', 'error');
INSERT INTO `logs` VALUES (113, '/?page=2', '127.0.0.1', '{\"page\": \"2\"}', 1627830924, 1, '', 'error');
INSERT INTO `logs` VALUES (114, '/?page=2', '127.0.0.1', '{\"page\": \"2\"}', 1627830941, 1, '', 'error');
INSERT INTO `logs` VALUES (115, '/?page=2', '127.0.0.1', '{\"page\": \"2\"}', 1627830942, 1, '', 'error');
INSERT INTO `logs` VALUES (116, '/?page=2', '127.0.0.1', '{\"page\": \"2\"}', 1627830997, 1, '', 'error');
INSERT INTO `logs` VALUES (117, '/?page=2', '127.0.0.1', '{\"page\": \"2\"}', 1627831052, 1, '', 'error');
INSERT INTO `logs` VALUES (118, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831122, 1, '', 'error');
INSERT INTO `logs` VALUES (119, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831157, 1, '', 'error');
INSERT INTO `logs` VALUES (120, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831165, 1, '', 'error');
INSERT INTO `logs` VALUES (121, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831174, 1, '', 'error');
INSERT INTO `logs` VALUES (122, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831191, 1, '', 'error');
INSERT INTO `logs` VALUES (123, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831240, 1, '', 'error');
INSERT INTO `logs` VALUES (124, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831437, 1, 'unsupported operand type(s) for *: \'range\' and \'int\'', 'error');
INSERT INTO `logs` VALUES (125, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831817, 1, '', 'error');
INSERT INTO `logs` VALUES (126, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627831891, 1, '', 'error');
INSERT INTO `logs` VALUES (127, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627832041, 1, '', 'error');
INSERT INTO `logs` VALUES (128, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627832042, 1, '', 'error');
INSERT INTO `logs` VALUES (129, '/?page=1', '127.0.0.1', '{\"page\": \"1\"}', 1627832055, 1, '', 'error');
COMMIT;

-- ----------------------------
-- Table structure for notifications
-- ----------------------------
DROP TABLE IF EXISTS `notifications`;
CREATE TABLE `notifications` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(191) NOT NULL,
  `content` longtext,
  `is_read` int(10) unsigned NOT NULL,
  `create_time` int(11) NOT NULL,
  `update_time` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `notifications_user_id_468e288d_fk_users_id` (`user_id`),
  CONSTRAINT `notifications_user_id_468e288d_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of notifications
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `topic_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tags_topic_id_b338c498_fk_topics_id` (`topic_id`),
  KEY `tags_user_id_cc865b26_fk_users_id` (`user_id`),
  CONSTRAINT `tags_topic_id_b338c498_fk_topics_id` FOREIGN KEY (`topic_id`) REFERENCES `topics` (`id`),
  CONSTRAINT `tags_user_id_cc865b26_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of tags
-- ----------------------------
BEGIN;
INSERT INTO `tags` VALUES (1, '标签', 4, 2);
INSERT INTO `tags` VALUES (2, 'django', 4, 2);
INSERT INTO `tags` VALUES (6, 'Django', 5, 1);
INSERT INTO `tags` VALUES (7, 'CBV', 5, 1);
INSERT INTO `tags` VALUES (8, 'bbs', 6, 1);
COMMIT;

-- ----------------------------
-- Table structure for topics
-- ----------------------------
DROP TABLE IF EXISTS `topics`;
CREATE TABLE `topics` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(64) NOT NULL,
  `body` longtext,
  `reply_count` int(10) unsigned NOT NULL,
  `view_count` int(10) unsigned NOT NULL,
  `sort` int(10) unsigned NOT NULL,
  `create_time` int(10) unsigned NOT NULL,
  `update_time` int(10) unsigned DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `topics_category_id_c30989a7_fk_categories_id` (`category_id`),
  KEY `topics_user_id_ac0579ca_fk_users_id` (`user_id`),
  CONSTRAINT `topics_category_id_c30989a7_fk_categories_id` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `topics_user_id_ac0579ca_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of topics
-- ----------------------------
BEGIN;
INSERT INTO `topics` VALUES (2, 'Java', '<p>JAVA</p>', 0, 1, 0, 1626700120, NULL, 1, 2);
INSERT INTO `topics` VALUES (3, 'PHP', '<p>PHP</p>', 0, 2, 0, 1626875251, NULL, 1, 2);
INSERT INTO `topics` VALUES (4, '标签', '<p>标签添加</p>', 0, 63, 0, 1626875755, NULL, 2, 2);
INSERT INTO `topics` VALUES (5, 'Django DeleteView 删除', '<pre>\n{% extends &#39;layout/app.html&#39; %}\n\n{% block title %}\n    文章标题\n{% endblock %}\n\n{% block content %}\n    &lt;div class=&quot;row&quot;&gt;\n\n        &lt;div class=&quot;col-lg-3 col-md-3 hidden-sm hidden-xs author-info&quot;&gt;\n            &lt;div class=&quot;card &quot;&gt;\n                &lt;div class=&quot;card-body&quot;&gt;\n                    &lt;div class=&quot;text-center&quot;&gt;\n                        作者：{{ topic.user.username }}\n                    &lt;/div&gt;\n                    &lt;hr&gt;\n                    &lt;div class=&quot;media&quot;&gt;\n                        &lt;div align=&quot;center&quot;&gt;\n                            &lt;a href=&quot;&quot;&gt;\n                                &lt;img class=&quot;thumbnail img-fluid&quot; src=&quot;/media/{{ topic.user.avatar }}&quot; width=&quot;300px&quot;\n                                     height=&quot;300px&quot;&gt;\n                            &lt;/a&gt;\n                        &lt;/div&gt;\n                    &lt;/div&gt;\n                &lt;/div&gt;\n            &lt;/div&gt;\n        &lt;/div&gt;\n\n        &lt;div class=&quot;col-lg-9 col-md-9 col-sm-12 col-xs-12 topic-content&quot;&gt;\n            &lt;div class=&quot;card&quot;&gt;\n                &lt;div class=&quot;card-body&quot;&gt;\n                    &lt;h1 class=&quot;text-center mt-3 mb-3&quot;&gt;\n                        {{ topic.title }}\n                    &lt;/h1&gt;\n\n                    &lt;div class=&quot;article-meta text-center text-secondary&quot;&gt;\n                        {% load mylabel %}\n                        {{ topic.create_time|timestamp }}\n                        &sdot;\n                        &lt;i class=&quot;far fa-comment&quot;&gt;&lt;/i&gt;\n                        {{ topic.reply_count }}\n                    &lt;/div&gt;\n\n                    &lt;div class=&quot;topic-body mt-4 mb-4&quot;&gt;\n                        {{ topic.body|safe }}\n                    &lt;/div&gt;\n\n                    &lt;!-- 判断是不是自己的文章 --&gt;\n                    {% if request.user.id == topic.user.id %}\n                        &lt;div class=&quot;operate&quot;&gt;\n                            &lt;hr&gt;\n                            &lt;a href=&quot;{% url &#39;edit_topic&#39; topic.id %}&quot; class=&quot;btn btn-outline-secondary btn-sm&quot;\n                               role=&quot;button&quot;&gt;\n                                &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt; 编辑\n                            &lt;/a&gt;\n\n                            &lt;button type=&quot;button&quot; data-topic_id=&quot;{{ topic.id }}&quot;\n                                    class=&quot;btn_delete_topic btn btn-outline-secondary btn-sm&quot;&gt;\n                                &lt;i class=&quot;fa fa-trash&quot;&gt;&lt;/i&gt; 删除\n                            &lt;/button&gt;\n                        &lt;/div&gt;\n                    {% endif %}\n                &lt;/div&gt;\n            &lt;/div&gt;\n\n            &lt;!-- 用户回复列表 --&gt;\n            &lt;div class=&quot;card topic-reply mt-4&quot;&gt;\n                &lt;div class=&quot;card-body&quot;&gt;\n                    {% include &#39;topics/_reply_box.html&#39; %}\n                    {#                    {% include &#39;topics/_reply_list.html&#39; %}#}\n                &lt;/div&gt;\n            &lt;/div&gt;\n\n        &lt;/div&gt;\n    &lt;/div&gt;\n{% endblock %}\n\n{% block js %}\n    &lt;script&gt;\n        $(document).on(&quot;click&quot;, &quot;.btn_delete_topic&quot;, function () {\n            var topic_id = $(this).data(&quot;topic_id&quot;);\n            if (!topic_id) {\n                layer.msg(&quot;文章id参数缺失&quot;);\n                return false;\n            }\n            layer.confirm(&quot;你确定要删除吗&quot;, {\n                btn: [&#39;确定&#39;, &#39;取消&#39;],\n                title: &quot;提示&quot;\n            }, function () {\n                request(&quot;{% url &#39;delete_topic&#39; %}&quot;, {\n                    data: {\n                        &quot;topic_id&quot;: topic_id,\n                        &quot;csrfmiddlewaretoken&quot;: &quot;{{ csrf_token }}&quot;,\n                    },\n                    type: &quot;DELETE&quot;,\n                    dataType: &quot;json&quot;,\n                }, &quot;{% url &#39;blog_center&#39; request.user.username %}&quot;);\n            });\n        });\n    &lt;/script&gt;\n{% endblock %}\n\n</pre>', 0, 202, 0, 1626969745, 1627186693, 1, 1);
INSERT INTO `topics` VALUES (6, '测试BBS开发完成公告', '<p>测试BBS开发完成公告</p>', 0, 0, 0, 1627813316, NULL, 4, 1);
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nickname` varchar(50) DEFAULT NULL,
  `avatar` varchar(100) NOT NULL,
  `last_login_ip` varchar(64) NOT NULL,
  `update_time` int(11) DEFAULT NULL,
  `sex` int(10) unsigned NOT NULL,
  `email` varchar(64) NOT NULL,
  `mobile` varchar(11) DEFAULT NULL,
  `birthday` datetime(6) DEFAULT NULL,
  `introduction` longtext,
  `github` varchar(255) DEFAULT NULL,
  `qq` varchar(12) DEFAULT NULL,
  `sign` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('pbkdf2_sha256$150000$MtOdr0FCJla8$aI3/nAqNYBwNL3e74HhNAbv+IyGWuv5kGHIHBo0iEsM=', '2021-08-01 23:11:29.337762', 0, 'wujie', '', '', 0, 1, '2021-07-13 20:48:10.347939', 1, '', 'avatar/202107/20210715233812_12.jpg', '127.0.0.1', NULL, 1, '1418667580@qq.com', NULL, NULL, '无解', '', NULL, '无解的人生');
INSERT INTO `users` VALUES ('pbkdf2_sha256$150000$BJVaHJ46prMP$ILh9831f5ybHded5PdnGMVevOvQ3ZTMDkqJaNLjXe0Y=', '2021-07-28 21:44:50.143102', 0, 'wxvirus', '', '', 0, 1, '2021-07-19 20:23:33.803611', 2, NULL, 'avatar/202107/20210728214540_39.jpg', '127.0.0.1', NULL, 0, '', NULL, NULL, NULL, NULL, NULL, NULL);
COMMIT;

-- ----------------------------
-- Table structure for users_groups
-- ----------------------------
DROP TABLE IF EXISTS `users_groups`;
CREATE TABLE `users_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `users_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_users_id_group_id_83a49e68_uniq` (`users_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_users_id_1e682706_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of users_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for users_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `users_user_permissions`;
CREATE TABLE `users_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `users_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_users_id_permission_id_d7a00931_uniq` (`users_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_users_id_e1ed60a2_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of users_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;

```

