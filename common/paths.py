# coding: utf-8
import os
home_path = os.path.expanduser('~')
server_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


# 定义日志路径
def logging_path(module):
    log_path = os.path.join(home_path, 'logs', module)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return log_path
