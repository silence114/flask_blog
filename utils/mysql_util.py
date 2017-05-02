#!/usr/bin/python
# -*- coding:utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config_util import ConfigUtil


class MysqlUtil:
    def __init__(self):
        conf = ConfigUtil()
        host = conf.get_config(conf='host', section='db_info')
        port = conf.get_config(conf='port', section='db_info')
        username = conf.get_config(conf='username', section='db_info')
        password = conf.get_config(conf='password', section='db_info')
        database = conf.get_config(conf='database', section='db_info')
        charset = conf.get_config(conf='charset', section='db_info')

        self.DB_CONNECT_STRING = 'mysql+mysqldb://{username}:{password}@{host}:{port}/{database}?charset={charset}'.format(
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
            charset=charset
        )

    def get_engine(self):
        print self.DB_CONNECT_STRING
        engine = create_engine(self.DB_CONNECT_STRING, echo=True)
        if engine is not None:
            return engine
        else:
            raise Exception(u'无法链接数据库')

    def get_session(self):
        db_session = sessionmaker(bind=self.get_engine())
        session = db_session()
        if session is not None:
            return session
        else:
            raise Exception(u'无法创建数据库链接!')
