# -*- coding:utf-8 -*-
import os
import sys
import logging


class LoggingUtil:
    def __init__(self):
        log_conf_file_path = os.path.sep.join([sys.path[0], '..', 'conf', 'logging_config.ini'])   # 获取日志配置的路径
        logging.config.fileConfig(log_conf_file_path)
        self.logger = logging.getLogger("logging")

    def get_logger(self):
        return self.logger
