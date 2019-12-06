# coding:utf-8
from src.businesses.base.pub_web import GlobalBaseHandler
from src.db_models.models import IllegalAccessStats


class IllegalStats(GlobalBaseHandler):
    def get(self):
        """
        获取接入，发布统计数据
        :return:
        """
        date = self.get_argument("date")
        current_page = self.get_argument("current_page")  # 当前页
        if date:
            return self.query_by_date(date)
        elif current_page:
            return self.query_paginate(current_page)
        # 默认返回第一页的数据
        else:
            return self.query_paginate()

    def query_paginate(self, current_page=None):
        if current_page is None:
            current_page = 1
        else:
            current_page = int(current_page)
        #
        page_size = 5  # 分页条数
        # 总记录数, 总页数
        total_count = IllegalAccessStats.query_count(self.session)
        if total_count % page_size == 0:
            total_page = int(total_count / page_size)
        else:
            total_page = int(total_count / page_size) + 1

        # 小于第一页
        if current_page <= 0:
            current_page = 1
        # 大于最后一页
        if total_page > 0:
            if current_page > total_page:
                current_page = total_page
        else:
            current_page = 1

        # 当前页的数据
        stats_list = IllegalAccessStats.query_paginate(self.session, current_page=current_page, page_size=page_size)
        return self.render("statistics.html", stats_list=stats_list, date="", total_count=total_count,
                           total_page=total_page, current_page=current_page)

    def query_by_date(self, date):
        stats_list = IllegalAccessStats.query_by_date(self.session, date=date)
        #
        return self.render("statistics.html", stats_list=stats_list, date=date, total_count=None, total_page=None,
                           current_page=None)
