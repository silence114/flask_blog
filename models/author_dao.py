#!/usr/bin/python
# -*- coding:utf-8 -*-

from models import Author
from utils.mysql_util import MysqlUtil

class AuthorDAO():
    def __init__(self):
        self.session = MysqlUtil().get_session()

    def get_authors(self):
        return self.session.query(Author).all()

    def get_author_by_name(self, auth_name):
        return self.session.query(Author).filter_by(name=auth_name).first()

    def get_author_by_id(self, auth_id):
        return self.session.query(Author).filter_by(id=auth_id).first()

    def add_author(self, auth_name):
        if self.get_author_by_name(auth_name) is None:
            auth = Author(name=auth_name)
            self.session.add(auth)
            self.session.commit()
            return True, u'添加成功'
        else:
            return False, u'作者已经存在!'

    def delete_author(self, auth_name):
        auth = self.get_author_by_name(auth_name)
        if auth is None:
            return False, u'作者不存在!'
        self.session.delete(auth)
        self.session.commit()
        return True, u'删除作者成功!'

    def update_author(self, auth_id,auth_name):
        auth = self.get_author_by_name(auth_name)
        if auth is not None:
            return False, u'作者名已经存在!'
        else:
            auth = self.get_author_by_id(auth_id)
            auth.name = auth_name
            self.session.commit()
            return True, u'修改成功!'
