from django.core.cache import cache
from django.shortcuts import redirect, render

from djangoBBS import http_status_code
from utils.json_response import Show


def check_login(func):
    """
    验证登录
    :param func:
    :return:
    """

    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return Show.fail("请前去登录", None, http_status_code.AJAX_LOGIN_REQUIRED)
            else:
                return redirect("login")

    return wrapper


def redis_cache(key, timeout):
    """
    获取redis缓存的装饰器
    :param key: 键
    :param timeout: 过期时间
    :return:
    """

    def __redis_cache(func):
        def wrapper(*args, **kwargs):
            # 判断缓存是否存在
            print('check key: %s' % key)
            # cache.has_key(key):
            if key in cache:
                print('get cache')
                data = cache.get(key)
            else:
                # 若不存在则执行获取数据的方法
                # 注意返回数据的类型(字符串，数字，字典，列表均可)
                print('get data')
                data = func(*args, **kwargs)
                print('set cache')
                cache.set(key, data, timeout)
            return data

        return wrapper

    return __redis_cache


def observe_user(func):
    """
    观察当前用户是否操作的是当前用户的信息
    :param func:
    :return:
    """

    def wrapper(request, user_id):
        if request.user.id != user_id:
            return render(request, 'layout/404.html', {"exception": "当前操作对象非当前用户,请操作自己的信息资料!"})
        else:
            return func(request, user_id)

    return wrapper
