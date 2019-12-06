# coding: utf-8
import logging
from sqlalchemy import func, ForeignKey, Column, Index, event, Date, UniqueConstraint, SMALLINT
from sqlalchemy.types import String, Integer, DateTime, DECIMAL
from sqlalchemy import BIGINT
from sqlalchemy import Text
from src.db_models import MapBase


class TimeBaseModel(object):
    """模型基类，为模型补充创建时间与更新时间"""
    # mysql 5.5 不兼容，后面有时间再摸索
    # create_time = Column(DateTime, nullable=False, server_default=func.now())  # 记录的创建时间
    # update_time = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())  # 记录的更新时间

    create_time = Column(DateTime, nullable=False, default=func.now())  # 记录的创建时间
    update_time = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())  # 记录的更新时间


class IllegalAccessStats(TimeBaseModel, MapBase):
    __tablename__ = "illegal_access_stats"
    stats_keys = ["access_received_total", "access_inserted_total", "publish_received_total", "publish_send_total"]

    id = Column(Integer, primary_key=True, nullable=True, autoincrement=True)
    date = Column(Date, nullable=False)  # 统计日期， 例如：2019-08-30

    access_received_total = Column(Integer, nullable=True, server_default="0")  # 接入接收数据统计
    access_inserted_total = Column(Integer, nullable=True, server_default="0")  # 接入插入数据统计

    read_success_total = Column(Integer, nullable=True, server_default="0")  # 接入读取数据统计
    read_false_total = Column(Integer, nullable=True, server_default="0")
    download_success_total = Column(Integer, nullable=True, server_default="0")  # 接入下载数据统计
    download_false_total = Column(Integer, nullable=True, server_default="0")
    write_success_total = Column(Integer, nullable=True, server_default="0")  # 接入推送数据统计
    write_false_total = Column(Integer, nullable=True, server_default="0")

    publish_received_total = Column(Integer, nullable=True, server_default="0")  # 发布接收数据统计
    publish_send_total = Column(Integer, nullable=True, server_default="0")  # 发布发送数据统计

    def to_dict(self):
        return {
            "date": str(self.date),
            "access_received_total": self.access_received_total,
            "access_inserted_total": self.access_inserted_total,

            "read_success_total": self.read_success_total,
            "read_false_total": self.read_false_total,
            "download_success_total": self.download_success_total,
            "download_false_total": self.download_false_total,
            "write_success_total": self.write_success_total,
            "write_false_total": self.write_false_total,

            "publish_received_total": self.publish_received_total,
            "publish_send_total": self.publish_send_total
        }

    @classmethod
    def date_stats_exist(cls, date, session):
        exist_ret = session.query(cls).filter(cls.date == date).first()
        return bool(exist_ret)

    @classmethod
    def create_date_stats(cls, stats_info, session):
        record = cls(**stats_info)
        session.add(record)
        session.commit()
        return record

    @classmethod
    def stats_key_mapping(cls, stats_key):
        stats_key_mapping = {
            "access_received_total": cls.access_received_total,
            "access_inserted_total": cls.access_inserted_total,
            "publish_received_total": cls.publish_received_total,
            "publish_send_total": cls.publish_send_total
        }
        return stats_key_mapping[stats_key]

    @classmethod
    def update_total(cls, stats_key, date, count, session):
        current_stats_key = cls.stats_key_mapping(stats_key)
        session.query(cls).filter(cls.date == date).update({stats_key: current_stats_key + count})
        session.commit()
        return 1

    @classmethod
    def query_by_date(cls, session, date):
        obj_list = session.query(cls).filter(cls.date == date).all()
        #
        stats_data_list = []
        for obj in obj_list:
            stats_data = obj.to_dict()
            stats_data_list.append(stats_data)
        return stats_data_list

    @classmethod
    def query_paginate(cls, session, current_page, page_size):
        """
        :param session: 数据库会话
        :param current_page: 当前页数
        :param page_count: 每页条数
        :return:
        """
        query_set = session.query(cls)
        # 总记录数
        # total_count = query_set.count()
        # 分页处理
        obj_list = query_set.order_by(cls.date.desc())\
                            .limit(page_size).offset((current_page - 1) * page_size)\
                            .all()
        #
        stats_data_list = []
        for obj in obj_list:
            stats_data = obj.to_dict()
            stats_data_list.append(stats_data)
        return stats_data_list

    @classmethod
    def query_count(cls, session):
        """
        查询总数量
        :param session:
        :return:
        """
        total_count = session.query(cls).count()
        return total_count


# 数据库初始化
def init_db_data():
    MapBase.metadata.create_all()
    logging.info("init mysql_db success")
