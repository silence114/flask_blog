# -*- coding:utf-8 -*-
import sys
import os
import ConfigParser
import collections


class ConfigUtil:
    def __init__(self):
        self.Configurations = collections.defaultdict()
        self.sys_conf_file_path = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), '..', 'conf', 'sys_config.ini'])  # 获取配置文件的路径
        if os.path.exists(self.sys_conf_file_path) and os.path.isfile(self.sys_conf_file_path):
            self.conf = ConfigParser.ConfigParser()
            self.conf.read(self.sys_conf_file_path)
        else:
            exit(-1, 'can not find System config file:{log_file}'.format(log_file=self.sys_conf_file_path))

    def get_config(self, conf, section='default'):
        """
        从系统配置文件中获取配置信息
        :param conf: 配置项名称
        :param section: 配置项的段
        :return: 配置文件中的配置信息,如果不存在返回None
        """
        if self.conf.get(section, conf) is None:
            self.logger.error('can not find configuration {section}.{conf} in system config file'
                              .format(section=section, conf=conf))
            return None
        else:
            return self.conf.get(section, conf)

    def set_config(self, conf, vaule, section='default'):
        """
        修改配置文件中的配置项
        :param conf: 配置名称
        :param vaule: 修改后的配置值
        :param section: 配置section信息
        :return: None
        """
        self.conf.set(section, conf, vaule)
        self.conf.write(open(self.sys_conf_file_path, "w"))  # 配置项写回配置文件中

    def has_config(self, conf, section='default'):
        """
        判断配置文件中是否存在指定的配置项
        :param conf: 配置项名称
        :param section: 配置项所属的section
        :return: 如果存在返回True,不存在返回False
        """
        return self.get_config(conf, section) is None

    def has_section(self, section):
        """
        判断系统配置文件中是否存在section信息
        :param section: 查询的section名称
        :return: 如果存在返回True,不存在返回False
        """
        return self.conf.has_section(section)
