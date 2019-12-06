import datetime
from datetime import date
import tornado.web
from tornado.escape import xhtml_escape
import traceback


class BaseHandler(tornado.web.RequestHandler):
    """
    通用的请求处理基类，主要定义了一些API通信规范和常用的工具
    响应处理：
       一个请求在逻辑上分为三个结果：请求错误、请求失败和请求成功。请求错误会通常
       是由于请求不合法（如参数错误、请求不存在、token无效等），直接返回http状
       态码；请求失败通常是由于一些事物逻辑上的错误，比如库存不够、余额不足等；请
       求成功不解释

       错误请求: send_error(status_code, **kargs)[tornado自带，直接响应响应的HTTP错误头，如果你需要自定义错误Page的话，重写write_error(status_code, **kargs)]
       请求失败: send_fail(fail_code, fail_text)[返回JSON数据格式: {"success":False, "code":fail_code, "text":fail_text}]
       请求成功: send_success(**kwargs)[返回JSON数据格式:{"success":True, **kwargs}]

    请求处理工具：
       check_arguments:获取请求里的参数数据，并存在self.args里
    """

    def __init__(self, application, request, **kwargs):
        self.args = []
        super().__init__(application, request, **kwargs)

    def data_received(self, chunk):
        pass

    def format_text(self, raw_text):
        """
        @ raw_text: 未经任何处理的文本
        @ return: 经过xhtml_escape，和支持空白换行等多种操作后的html代码
        """
        rules = {" ": "&nbsp;","\n": "<br />"}
        x_text = xhtml_escape(raw_text)
        out_text = ""
        for c in x_text:
            if c in rules:
                out_text += rules[c]
            else:
                out_text += c
        return out_text

    def get_argument(self, name, default=None, strip=True):
        if self.request.method.upper() in ["POST", "PUT", "DELETE"] and\
           "Content-Type" in self.request.headers and \
           self.request.headers["Content-Type"].split(";")[0].strip() \
           == "application/json":
            if not hasattr(self, "_json_parsed_dict"):
                try:
                    self._json_parsed_dict = tornado.escape.json_decode(self.request.body)
                except:
                    traceback.print_exc()
                    self._json_parsed_dict = {}
            if name in self._json_parsed_dict:
                return self._json_parsed_dict[name]
            # 没找着，pass
        return super().get_argument(name, default, strip)

    def check_arguments(*request_arguments):
        """
        @Decorator( request_arguments:string(...) )
        这个装饰器可以配合 Handler 进行参数的检查
        每一个参数是一个字符串，形如 name[:type][?]
        type是类型，可以为 int，str等，? 代表参数是否可选
        参数会从请求的url中解析，或从post的body中以json的方式寻找
        """
        def func_wrapper(method):
            def wrapper(self, *args, **kwargs):
                obj = dict()
                for name in request_arguments:
                    if name.count(':'):
                        Type = name.split(":")[1]
                        name = name.split(":")[0]
                    else:
                        Type = "all"
                    should_exists = True
                    if name.count("?") > 0 or Type.count("?") > 0:
                        name = name.replace("?", '')
                        Type = Type.replace("?", '')
                        should_exists = False
                    # 获取参数
                    try:
                        v = self.get_argument(name)
                    except:
                        if should_exists:
                            return self.send_error(400, error_msg=name)
                        else:
                            continue
                    # 解析参数
                    try:
                        v = self.__parse_type(v, Type)
                    except:
                        if should_exists:
                            return self.send_error(400, error_msg=name)
                        else:
                            continue
                    # 存储
                    obj[name] = v
                self.args = obj
                return method(self, *args, **kwargs)
            return wrapper
        return func_wrapper

    def send_success(self, **kwargs):
        obj = {"success": True,
               "data": {}}
        for k in kwargs:
            obj["data"][k] = kwargs[k]
        self.write(obj)

    def send_fail(self, error_text=None, error_code=None, error_redirect=None):
        if type(error_code) == int:
            res = {"success": False, "error_code": error_code, "error_text": error_text, "error_redirect": error_redirect}
        else:
            res = {"success": False, "error_text": error_text}
        self.set_header("Content-Type", 'utf-8')
        self.write(res)

    def __parse_type(self, value, Type):
        if value is None:
            raise Exception()
        if not Type or Type == "all":
            return value
        if Type == "str" and type(value) != str:
            return str(value)
        if Type == "int" and type(value) != int:
            return int(value)
        if Type == "float" and type(value) != float:
            return float(value)
        if Type == "number" and type(value) != int and type(value) != float:
            try: return int(value)
            except: pass
            try: return float(value)
            except: pass
            raise Exception()
        if Type == "list" and type(value) != list:
            return list(value)
        if Type == "dict" and type(value) != dict:
            return dict(value)
        if Type == "bool" and type(value) != bool:
            if type(value) == str:
                value = value.lower()
                if value == "true":
                    return True
                else:
                    return False
            elif type(value) == int:
                return int(value)
            return False
        if Type == "date" and type(value) != date:
            return datetime.datetime.strptime(value, "%Y-%m-%d").date()
        if Type == "datetime" and type(value) != datetime:
            return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

        return value
