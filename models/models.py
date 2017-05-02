#!/usr/bin/python
# -*- coding:utf-8 -*-

from utils.mysql_util import MysqlUtil
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, TIMESTAMP
from app import login_manager
from flask.ext.login import UserMixin
import datetime
import json
BaseModel = declarative_base()


class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)                           # 用户昵称
    password = Column(String(128), nullable=False)                          # 用户密码hash
    email = Column(String(32), nullable=False, unique=True)                 # 用户注册邮箱
    status = Column(Integer, default=0)
    is_admin = Column(Integer, default=0)
    register_time = Column(DateTime, default=datetime.datetime.utcnow)     # 用户注册时间
    last_login_time = Column(DateTime, default=datetime.datetime.utcnow)   # 用户最近登录时间

    def __repr__(self):
        return 'id:{id},username:{username},email:{email},password:{password},register_time={time}'.format(
            id=self.id,
            username=self.username,
            password=self.password,
            time=self.register_time,
            email=self.email
        )


class Note(BaseModel):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String(2048))
    note_time = Column(DateTime(), default=datetime.datetime.now)


class Category(BaseModel):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, unique=True)
    cate_name = Column(String(32), unique=True)


class Article(BaseModel):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(128), unique=True, nullable=False)
    is_public = Column(Integer(), default=1)
    intro = Column(String(516), nullable=False)
    auth_name = Column(String(32), nullable=False)
    auth_id = Column(Integer(), nullable=False)
    file_path = Column(String(128), nullable=False)
    tags = Column(String(128), nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    modified_time = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    BaseModel.metadata.create_all(MysqlUtil().get_engine())


# flask-login 回调函数
@login_manager.user_loader
def load_user(user_id):
    from users_dao import UsersDAO
    user_dao = UsersDAO()
    return user_dao.get_user_by_id(user_id)
