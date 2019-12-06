# coding: utf-8
from __future__ import absolute_import
import os
from logging import Formatter, getLogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
from cloghandler import ConcurrentRotatingFileHandler
from common.paths import logging_path

# 日志最低记录级别1-DEBUG 2-INFO 3-WARNING 4-ERROR 5-CRITICAL
LOGGER_SET_LEVEL = 1

# debug日志rotate存留数
DEBUG_BACK_COUNT = 5
# info日志rotate存留数
INFO_BACK_COUNT = 5
# warning日志rotate存留数
WARNING_BACK_COUNT = 5
# error日志rotate存留数
ERROR_BACK_COUNT = 5
# critical日志rotate存留数
CRITICAL_BACK_COUNT = 1
# 单个日志文件大小（单位Bytes） 500M
LOGGER_FILE_MAXBYTE = 500 * 1024 * 1024


def logger_init(log_path=logging_path('http_server_log')):
    formatter = Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

    debug = ConcurrentRotatingFileHandler(
        os.path.join(log_path, 'debug.log'),
        maxBytes=LOGGER_FILE_MAXBYTE,
        backupCount=DEBUG_BACK_COUNT)
    debug.setLevel(DEBUG)
    debug.setFormatter(formatter)

    info = ConcurrentRotatingFileHandler(
        os.path.join(log_path, 'info.log'),
        maxBytes=LOGGER_FILE_MAXBYTE,
        backupCount=INFO_BACK_COUNT)
    info.setLevel(INFO)
    info.setFormatter(formatter)

    warning = ConcurrentRotatingFileHandler(
        os.path.join(log_path, 'warning.log'),
        maxBytes=LOGGER_FILE_MAXBYTE,
        backupCount=WARNING_BACK_COUNT)
    warning.setLevel(WARNING)
    warning.setFormatter(formatter)

    error = ConcurrentRotatingFileHandler(
        os.path.join(log_path, 'error.log'),
        maxBytes=LOGGER_FILE_MAXBYTE,
        backupCount=ERROR_BACK_COUNT)
    error.setLevel(ERROR)
    error.setFormatter(formatter)

    critical = ConcurrentRotatingFileHandler(
        os.path.join(log_path, 'critical.log'),
        maxBytes=LOGGER_FILE_MAXBYTE,
        backupCount=CRITICAL_BACK_COUNT)
    critical.setLevel(CRITICAL)
    crit_format = Formatter('%(asctime)s %(message)s')
    critical.setFormatter(crit_format)

    logger = getLogger('')
    logger.addHandler(debug)
    logger.addHandler(info)
    logger.addHandler(warning)
    logger.addHandler(error)
    logger.addHandler(critical)
    if LOGGER_SET_LEVEL == 2:
        LEVEL = INFO
    elif LOGGER_SET_LEVEL == 3:
        LEVEL = WARNING
    elif LOGGER_SET_LEVEL == 4:
        LEVEL = ERROR
    elif LOGGER_SET_LEVEL == 5:
        LEVEL = CRITICAL
    else:
        LEVEL = DEBUG
    logger.setLevel(LEVEL)
