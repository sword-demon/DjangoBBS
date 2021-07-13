import json


def get_city_name_by_ip(ip):
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


a = get_city_name_by_ip("127.0.0.1")
print(a)
