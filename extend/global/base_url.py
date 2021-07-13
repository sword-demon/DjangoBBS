from djangoBBS.dev import BASE_URL
from djangoBBS.dev import DEFAULT_BLANK_AVATAR


def base_url(request):
    return {
        "base_url": BASE_URL
    }


def default_avatar(request):
    return {
        "default_avatar": DEFAULT_BLANK_AVATAR
    }