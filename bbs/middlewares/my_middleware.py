import json
import time

from django.db.models import F
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from bbs.models import Log, Topics
from djangoBBS import settings

import logging

from utils.tools import get_ip

logger = logging.getLogger('api_track')
logger_time = logging.getLogger('api_timeout')
logger_error = logging.getLogger("api_error")


class DataRecordMiddleware(MiddlewareMixin):
    """
    全局异常日志记录
    """

    def get_request_method(self, request):
        return request.get_full_path()

    def process_exception(self, request, exception):
        api = self.get_request_method(request)
        ip = get_ip(request)
        request_method = request.method

        input_params = []
        user_id = request.user.id if request.user.id else 1

        if request_method == "GET":
            input_params = request.GET.dict()
        elif request_method == "POST":
            input_params = request.POST.dict()
        ret = "服务器繁忙, 请稍后再试"
        error_msg = "API: %s 异常信息:%s " % (api, exception)
        logger_error.info(error_msg)

        self.log_record(api, ip, json.dumps(input_params), str(exception), 'error', user_id)

        if settings.DEBUG:
            return JsonResponse({"status": 0, 'msg': error_msg})
        else:
            return JsonResponse({'status': 0, 'msg': '%s' % ret})

    def log_record(self, request_path, ip, params, content, level, user_id=1):
        log = Log(request_path=request_path, ip=ip, params=params, content=content, level=level, user_id=user_id,
                  create_time=time.time())
        log.save()


class TopicViewObserver(MiddlewareMixin):
    """
    文章阅读观察者
    阅读量+1
    """

    def process_request(self, request):
        from django.urls import resolve
        path = request.path
        rm = resolve(path)
        url_name = rm.url_name
        if url_name == "topic_show":
            last_topic_id = path.strip("/").split("/")[2]
            # print(last_topic_id)
            # 查看文章阅读数自增
            Topics.objects.filter(id=int(last_topic_id)).update(view_count=F("view_count") + 1)
