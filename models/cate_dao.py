#!/usr/bin/python
# -*- coding:utf-8 -#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.mysql_util import MysqlUtil
from models import Category


class CategoryDAO:
    def __init__(self):
        user_dao = MysqlUtil()
        self.session = user_dao.get_session()


    def add_category(self, cate_name):
        if self.get_cate(cate_name) is None:
            cate = Category(cate_name=cate_name)
            self.session.add(cate)
            self.session.commit()
            return True, u'成功添加新分类'
        else:
            return False, u'类目已经存在'

    def get_cate(self, cate_name):
        cate = self.session.query(Category).filter_by(cate_name=cate_name).first()
        if cate is not None:
            return cate
        else:
            return None

    def get_categories(self):
        return self.session.query(Category).all()


if __name__ == '__main__':
    print '--------'
    cate = CategoryDAO()
    result, info = cate.add_category('hive')
    print '-----> ', info
    result, info = cate.add_category('hadoop')
    print '-----> ', info
    print '=====>', cate.get_cate('hive')
    print '-----> ', cate.get_categories()
