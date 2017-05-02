#!/usr/bin/python
# -*- coding:utf-8 -#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.mysql_util import MysqlUtil
from models import Category
import datetime


class CategoryDAO:
    def __init__(self):
        user_dao = MysqlUtil()
        self.session = user_dao.get_session()

    def add_category(self, cate_name):
        if self.get_cate_by_name(cate_name) is None:
            cate = Category(cate_name=cate_name)
            self.session.add(cate)
            self.session.commit()
            return True, u'成功添加新分类'
        else:
            return False, u'类目已经存在'

    def get_cate_by_name(self, cate_name):
        cate = self.session.query(Category).filter_by(cate_name=cate_name).first()
        if cate is not None:
            return cate
        else:
            return None

    def get_cate_by_id(self, cate_id):
        cate = self.session.query(Category).filter_by(id=cate_id).first()
        if cate is not None:
            return cate
        else:
            return None

    def get_categories(self):
        return self.session.query(Category).all()

    def delete_category(self, cate_id):
        cate = self.get_cate_by_id(cate_id)
        if cate is not None:
            self.session.delete(cate)
            self.session.commit()
            return True, u'删除成功'
        else:
            return False, u'删除失败,删除的类目不存在!'

    def update_category(self, cate_id, cate_name):
        cate = self.get_cate_by_id(cate_id)
        if cate is not None:
            if self.get_cate_by_id(cate_name) is None:
                cate.cate_name = cate_name
                cate.modify_time = datetime.datetime.utcnow()
                self.session.commit()
                return True, u'修改成功!'
            else:
                return False, u'修改的类目名称已经存在!'
        else:
            return False, u'指定ID的类目不存在!'



if __name__ == '__main__':
    print '--------'
    cate = CategoryDAO()
    result, info = cate.add_category('hive')
    print '-----> ', info
    result, info = cate.add_category('hadoop')
    print '-----> ', info
    print '=====>', cate.get_cate('hive')
    for cat in cate.get_categories():
        print cat.id,':',cat.cate_name

