# Django 开发 BBS + Blog

## 构建项目

```bash
django-admin startproject djangoBBS
```

## 导出当前项目需要的类库

```bash
# 安装
pip install pipreqs  # 或者 pip3 install pipreqs

# 使用
pipreqs .  # . 表示当前目录

# 使用建议，导出前先定位到当前项目根目录
pipreqs ./ --encoding=utf8 # 该命令避免编码错误
```

## 日志以及全局记录中间件

> 设计了一个记录全局异常的日志表，使用中间件进行记录，在开发环境时直接提示错误内容，在生成环境下，提示固定内容。

## 文章阅读量中间件

根据请求的地址反向获取url的别名来判断是否是访问了文章详情页。

获取url的别名

```python
def process_request(self, request):
    from django.urls import resolve
    path = request.path
    rm = resolve(path)
    url_name = rm.url_name
    print(url_name)
```

就可以获取urls.py里给path设置的`name`属性的值。

## ImageStorage

> 重写Django的文件存储`save`方法，防止同一时间里并发上传文件时文件名重复的问题。
>

## 模板继承

使用了模板继承，将公共部分的页面进行分离。 对很多冗长的页面，使用`include`进行加载，进行分割页面代码。做到短小简练。

## JS封装了request请求方法

在全局异常处理的中间件里，我返回的内容是`json`格式的提示语， 所以，我直接写一个基本所有页面使用的`ajax`提交的信息回调函数处理格式。

```javascript
function request(url, option = {}, redirect_uri = "") {
    $.ajax({
        url,
        ...option,
        success: function (res) {
            if (res.status === 1) {
                layer.msg(res.msg, {
                    icon: 6
                }, function () {
                    if (redirect_uri != "") {
                        window.location.href = redirect_uri;
                    } else {
                        window.location.reload();
                    }
                });
            } else if (res.status === 2) {
                layer.msg(res.msg, {icon: 5}, function () {
                    window.location.href = "{% url 'login' %}";
                });
            } else {
                var result;
                if (typeof res.msg == "string") {
                    result = res.msg;
                } else {
                    var str = "";
                    $.each(res.msg, function (index, item) {
                        str += "<br>" + item[0]
                    });
                    result = str;
                }
                layer.msg(result, {
                    icon: 5,
                    time: 2000
                }, function () {
                    window.location.reload();
                });
            }
        },
        error: function () {
            layer.msg("系统网络异常");
            return false;
        },
    });
}
```
>这里使用了`layui`的弹窗插件来让页面提示更加优美。

## 封装固定的返回json格式
```python
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

```

