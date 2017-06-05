#!/usr/bin/python
# -*- coding:utf-8 -*-

from utils.mysql_util import MysqlUtil
from utils.config_util import ConfigUtil
from werkzeug.security import generate_password_hash
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime
from app import login_manager
from flask.ext.login import UserMixin
import datetime
import MySQLdb

BaseModel = declarative_base()


class User(UserMixin, BaseModel):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), nullable=False)                           # 用户昵称
    password = Column(String(128), nullable=False)                          # 用户密码hash
    email = Column(String(32), nullable=False, unique=True)                 # 用户注册邮箱
    status = Column(Integer, default=0)
    is_admin = Column(Integer, default=0)
    register_time = Column(DateTime, default=datetime.datetime.now)     # 用户注册时间
    last_login_time = Column(DateTime, default=datetime.datetime.now)   # 用户最近登录时间

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
    create_time = Column(DateTime, default=datetime.datetime.now)  # 用户注册时间
    modify_time = Column(DateTime, default=datetime.datetime.now)  # 用户最近登录时间


class Article(BaseModel):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String(128), unique=True, nullable=False)
    is_public = Column(Integer(), default=1)
    intro = Column(String(516), nullable=False)
    auth_name = Column(String(32), nullable=False)
    auth_id = Column(Integer(), nullable=False)
    cate_id = Column(Integer(), nullable=False)
    cate_name = Column(String(128), nullable=False)
    file_path = Column(String(128), nullable=False)
    tags = Column(String(128), nullable=True)
    create_time = Column(DateTime, default=datetime.datetime.now)
    modified_time = Column(DateTime, default=datetime.datetime.now)


class Author(BaseModel):
    __tablename__='authors'
    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(128), unique=True, nullable=False)
    create_time = Column(DateTime, default=datetime.datetime.now)
    modified_time = Column(DateTime, default=datetime.datetime.now)


class Comment(BaseModel):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, unique=True)
    article_id = Column(Integer, nullable=False)
    user = Column(String(32), nullable=False)
    comment = Column(String(1024), nullable=False)
    good = Column(Integer, nullable=False, default=0)
    bad = Column(Integer, nullable=False, default=0)
    replay = Column(String(1024))
    create_time = Column(DateTime, default=datetime.datetime.now)
    modified_time = Column(DateTime, default=datetime.datetime.now)


def init_db():
    conf = ConfigUtil()
    host = conf.get_config(conf='host', section='db_info')
    port = conf.get_config(conf='port', section='db_info')
    username = conf.get_config(conf='username', section='db_info')
    password = conf.get_config(conf='password', section='db_info')
    database = conf.get_config(conf='database', section='db_info')

    conn = MySQLdb.connect(host=host, user=username, passwd=password, port=int(port))
    cur = conn.cursor()
    sql = 'CREATE DATABASE IF NOT EXISTS `{db}` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'.format(db=database)

    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

    session = MysqlUtil().get_session()
    BaseModel.metadata.create_all(MysqlUtil().get_engine())

    email = conf.get_config('email', 'admin_account')
    if session.query(User).filter_by(email=email).first() is None:
        password = conf.get_config('password', 'admin_account')
        username = conf.get_config('username', 'admin_account')

        user = User(username=username,
                    password=generate_password_hash(password),
                    email=email,
                    status=1,
                    is_admin=1,
                    register_time=datetime.datetime.now(),
                    last_login_time=datetime.datetime.now())
        session.add(user)
        session.commit()


# flask-login 回调函数
@login_manager.user_loader
def load_user(user_id):
    from users_dao import UsersDAO
    user_dao = UsersDAO()
    return user_dao.get_user_by_id(user_id)
