# coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (sessionmaker)
from sqlalchemy import create_engine
from settings.setting import MYSQL_SERVER, MYSQL_DRIVER, MYSQL_USERNAME, MYSQL_PASSWORD, DB_NAME, DB_CHARSET

# MYSQL_USERNAME = os.getenv('MYSQL_USER') or settings.MYSQL_USERNAME
# MYSQL_PASSWORD =

# 数据库
engine = create_engine("mysql+{driver}://{username}:{password}@{server}/{database}?charset={charset}"
                       .format(driver=MYSQL_DRIVER,
                               username=MYSQL_USERNAME,
                               password=MYSQL_PASSWORD,
                               server=MYSQL_SERVER,
                               database=DB_NAME,
                               charset=DB_CHARSET),
                       pool_size=20,
                       max_overflow=100,
                       pool_recycle=1,
                       echo=False)
engine.execute("SET NAMES {charset};".format(charset=DB_CHARSET))
MapBase = declarative_base(bind=engine)
DBSession = sessionmaker(bind=engine)
