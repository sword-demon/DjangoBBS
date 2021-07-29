import random


def get_ip(request):
    """
    获取请求者的IP信息
    :param request:
    :return:
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def get_random_set(bits):
    num_set = [chr(i) for i in range(48, 58)]
    char_set = [chr(i) for i in range(97, 123)]
    total_set = num_set + char_set

    value_set = "".join(random.sample(total_set, bits))

    return value_set


def tree_list(datas):
    """
    获取树形结构
    """
    lists = []
    tree = {}
    parent_id = ''
    for i in datas:
        item = i
        tree[item['id']] = item
    root = None
    for i in datas:
        obj = i
        if not obj['pid_id']:
            root = tree[obj['id']]
            lists.append(root)
        else:
            parent_id = obj['pid_id']
            if 'childlist' not in tree[parent_id]:
                tree[parent_id]['childlist'] = []
            tree[parent_id]['childlist'].append(tree[obj['id']])
    return lists