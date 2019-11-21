# coding=utf8

#
# 日志
#

import logging
from datetime import datetime
import os

from .util_config import BASE_DIR

LOG_PATH = os.path.join(BASE_DIR, 'log')

complicated_formatter = logging.Formatter(
   # '%(asctime)s-%(name)s[%(levelname)s]:%(message)s')
    '%(message)s')
simple_formatter = logging.Formatter('[%(levelname)s]<%(threadName)s>:%(message)s')


def get_logger(log_name, has_file=False, log_level='DEBUG', formatter_str=None):
    level_map = {
        'DEBUG'   : logging.DEBUG,
        'INFO'    : logging.INFO,
        'WARNING' : logging.WARNING,
        'ERROR'   : logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    _level = log_level.upper().strip()
    level = level_map[_level]

    now_str = datetime.now().strftime('%Y-%m-%d')
    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    # 文件日志
    if has_file:
        # 创建log文件夹
        os.makedirs(LOG_PATH, exist_ok=True)
        file_path = os.path.join(LOG_PATH, '{}.log'.format(log_name))
        f_handler = logging.FileHandler(file_path, encoding='utf-8')
        if not formatter_str:
            f_handler.setFormatter(complicated_formatter)
        else:
            formatter = logging.Formatter(formatter_str)
            f_handler.setFormatter(formatter)

        logger.addHandler(f_handler)

    # 控制台打印
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(simple_formatter)
    logger.addHandler(c_handler)

    return logger


logger_hive = get_logger('news_all', True)