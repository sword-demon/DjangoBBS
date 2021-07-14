import datetime
import json

from django import template

register = template.Library()


@register.filter(is_safe=True)
def label_with_classes(value, arg):
    return value.label_tag(attrs={'class': arg})


@register.filter()
def widget_with_classes(value, arg):
    return value.as_widget(attrs={'class': arg})


@register.filter()
def min_nums(start_time):
    """
    计算当前时间点到上次登录时间之间的分钟数
    :param start_time:
    :return:
    """
    # 处理格式,加上秒位
    startTime1 = start_time
    now = datetime.datetime.now()
    # seconds = (endTime2 - startTime2).seconds
    # 来获取时间差中的秒数。注意，seconds获得的秒只是时间差中的小时、分钟和秒部分的和，并没有包含时间差的天数（既是两个时间点不是同一天，失效）
    total_seconds = (now - startTime1).total_seconds()
    # 来获取准确的时间差，并将时间差转换为秒
    mins = total_seconds / 60
    return int(mins)


@register.filter()
def get_sex(sex):
    """
    判断性别
    :param sex:
    :return:
    """
    if sex == 1:
        return "男"
    else:
        return "女"


@register.filter()
def get_city_name_by_ip(ip):
    """
    根据IP地址获取所在城市,没有传值或传值为空,则获取请求接口的当前用户的ip地址对应的城市
    :param ip:
    :return:
    """
    import requests
    url = "https://api.map.baidu.com/location/ip?ak=DaPovYeO1apmksvwBnp5N4OD&ip=%s&coor=bd09ll" % ip
    response = requests.get(url)
    json_data = json.loads(response.text)
    if json_data['status'] == 0:
        return json_data['content']['address']
    # print(response.text)
    # print(json.loads(response.text))
    else:
        return '未能定位'


@register.filter()
def get_url_name(path):
    """
    在模板中获取请求地址的url别名
    :param path:
    :return:
    """
    from django.urls import resolve

    rm = resolve(path)
    url_name = rm.url_name
    return url_name
