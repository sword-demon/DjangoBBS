from djangoBBS.dev import BASE_URL
from djangoBBS.dev import DEFAULT_BLANK_AVATAR


def base_url(request):
    """
    设置域名基础地址
    :param request:
    :return:
    """
    return {
        "base_url": BASE_URL
    }


def default_avatar(request):
    """
    设置默认的头像
    :param request:
    :return:
    """
    return {
        "default_avatar": DEFAULT_BLANK_AVATAR
    }
