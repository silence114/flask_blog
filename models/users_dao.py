#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.mysql_util import MysqlUtil
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
import re


class UsersDAO:
    def __init__(self):
        user_dao = MysqlUtil()
        self.session = user_dao.get_session()

    def verify_password(self, email, password):
        if password is None or len(password) == 0:
            return False, u'密码不能为空'
        if email is None or len(email) == 0:
            return False, u'用户注册邮箱不能为空'
        if not self.verify_email(email):
            return False, u'邮箱格式不满足规范!'

        password_hash = self.get_password(email)
        if password_hash is not None:
            return check_password_hash(password_hash, password)
        else:
            return False

    def get_password_by_email(self, email):
        user = self.session.query(User).filter_by(email=email).first()
        if user is not None:
            return user.password
        else:
            return None

    def get_user_by_email(self, email):
        user = self.session.query(User).filter_by(email=email).first()
        if user is not None:
            return user
        else:
            return None

    def get_user_by_id(self, user_id):
        user = self.session.query(User).filter_by(id=user_id).first()
        if user is not None:
            return user
        else:
            return None

    def verify_email(self, email):
        if email is None or len(email) == 0:
            return False, u'密码不能为空!'
        else:
            pattern = re.compile(u'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$')
            match = pattern.search('hello.world@163.com')
            if match:
                return True
            else:
                return False

    def add_user(self, user):
        self.session.add(user)
        self.session.commit()

    def confirm_email(self, email):
        user = self.get_user_by_email(email)
        if user is not None:
            print '---------->> user.status:', user.status
            if user.status != 1:
                user.status = 1
                self.session.add(user)
                self.session.commit()
                return True, None
            else:
                return False, u'邮箱已经确认,无需再次确认!'
        else:
            return False, u'该邮箱尚未注册过,非法确认邮件!!!'




