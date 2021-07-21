#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoBBS.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def init_categories():
    from bbs.models import Categories
    import time

    Categories.objects.all().delete()
    Categories.objects.create(name="分享", description="分享创造,分享发现", create_time=time.time())
    Categories.objects.create(name="教程", description="开发技巧、推荐扩展包等", create_time=time.time())
    Categories.objects.create(name="问答", description="请保持友善,互帮互助", create_time=time.time())
    Categories.objects.create(name="公告", description="站点公告", create_time=time.time())


if __name__ == '__main__':
    main()
    # init_categories()
