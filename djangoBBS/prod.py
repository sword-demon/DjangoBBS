import os

from djangoBBS.settings import BASE_DIR

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认是sqllite3,改为mysql
        # 创建空库后执行 python manage.py makemigrations
        # 生成迁移文件app/migrations/0001_initial.py
        # 会创建迁移文件里指定的表名name：
        # 执行python manage.py migrate完成数据迁移
        # 一般是建库建表后反向生成models模型文件:python manage.py inspectdb > app/models.py
        'NAME': 'django_bbs',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': '1',
        'PORT': '3306'
    }
}

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

BASE_URL = '生产环境的域名地址'
