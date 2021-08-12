# -*- coding: utf8 -*-
# @Time    : 2021/8/12 21:48
# @Author  : wxvirus
# @File    : db_router.py
# @Software: PyCharm
# 实现数据库读写路由

class MasterSlaveDBRouter(object):
    """
    数据库读写路由
    """

    def db_for_read(self, model, **hints):
        """
        读
        :param model:
        :param hints:
        :return:
        """
        return "slave"

    def db_for_write(self, model, **hints):
        """
        写
        :param model:
        :param hints:
        :return:
        """

        return "default"

    def allow_reloation(self, obj1, obj2, **hints):
        """
        是否运行关联操作
        :param obj1:
        :param obj2:
        :param hints:
        :return:
        """
        return True
