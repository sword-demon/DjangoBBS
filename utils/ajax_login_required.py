from django.shortcuts import redirect
from utils.json_response import Show


def check_login(func):
    def wrapper(request, *args, **kwargs):
        auth_user_id = request.session.get("_auth_user_id")
        if auth_user_id:
            return func(request, *args, **kwargs)
        else:
            if request.is_ajax():
                return Show.fail("请前去登录", None, 2)
            else:
                return redirect("login")

    return wrapper
