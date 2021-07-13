from django.http import JsonResponse


class HttpStatusCode(object):
    SUCCESS = 1
    FAIL = 0


class Show(HttpStatusCode):

    @staticmethod
    def success(message='OK', data=None):
        result = {
            "status": HttpStatusCode.SUCCESS,
            "msg": message,
            "data": data
        }

        return JsonResponse(result)

    @staticmethod
    def fail(message='error', data=None, status=HttpStatusCode.FAIL):
        result = {
            "status": status,
            "msg": message,
            "data": data
        }

        return JsonResponse(result)
