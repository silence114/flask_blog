#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.mysql_util import MysqlUtil
from sqlalchemy import desc
from models import Article

import datetime


class ArticleDao:
    def __init__(self):
        self.session = MysqlUtil().get_session()

    def get_articles(self, page=0, size=20):
        article_num = self.get_article_num()
        if page * size > article_num:
            return None, u'分页数超出最大值'
        info = u'more' if (page + 1) * size < article_num else u'nomore'
        return self.session.query(Article).order_by(desc(Article.modified_time)).offset(size * page).limit(size).all(), info

    def get_article_num(self):
        return self.session.query(Article).count()

    def get_article_by_title(self, title):
        return self.session.query(Article).filter_by(title=title).first()

    def get_article_by_id(self, id):
        return self.session.query(Article).filter_by(id=id).first()

    def new_article(self, title, author_id, author_name, cate_id, cate_name, intro, filepath, tags):
        article = Article(
            title=title,
            intro=intro,
            is_public=1,
            auth_id=author_id,
            auth_name=author_name,
            cate_id=cate_id,
            cate_name=cate_name,
            file_path=filepath,
            tags=tags,
            create_time=datetime.datetime.now(),
            modified_time=datetime.datetime.now()
        )

        if self.get_article_by_title(title) is None:
            self.session.add(article)
            self.session.commit()
            return True, u'成功添加新文章!'
        else:
            return False, u'文章标题已经存在!'

    def delete_article(self, article):
        self.session.delete(article)
        self.session.commit()
        return True, u'删除成功!'

    def get_articles_by_cate(self, cate, page=0, size=20):
        article_num = self.get_article_num()
        if page * size > article_num:
            return None, u'分页数超出最大值'
        info = u'more' if (page + 1) * size < article_num else u'nomore'
        return self.session.query(Article).filter_by(cate_id=cate).order_by(desc(Article.modified_time)).offset(size * page).limit(size).all(), info

    def get_article_by_tag(self, tag, page=0, size=20):
        article_num = self.get_article_num()
        if page * size > article_num:
            return None, u'分页数超出最大值'
        info = u'more' if (page + 1) * size < article_num else u'nomore'
        return self.session.query(Article)\
                   .filter(Article.tags.like('%{tag}%'.format(tag=tag)))\
                   .order_by(desc(Article.modified_time)).offset(size * page).limit(size).all(), info

if __name__ == '__main__':
    print ArticleDao().get_article_by_tag('hive')