# coding: utf-8
from src.db_models import DBSession
from src.businesses.base.webbase import BaseHandler


# 全局基类方法
class GlobalBaseHandler(BaseHandler):
    @property
    def session(self):
        if hasattr(self, "_session"):
            return self._session
        self._session = DBSession()
        return self._session

    # 关闭数据库会话
    def on_finish(self):
        if hasattr(self, "_session"):
            self._session.close()

    def prepare(self):
        # 防止请求头内容是application/json，实际内容不是json数据
        content_type = self.request.headers.get("Content-Type", "")
        if content_type.startswith("application/json"):
            self.body_data = self.request.body
        elif content_type.startswith("text/plain"):
            self.body_data = self.request.body
        else:
            self.body_data = ""
