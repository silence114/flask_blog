#!/usr/bin/python
# -*- coding:utf-8 -*-
from utils.mysql_util import MysqlUtil
from models import Article

class ArticleDao:
    def __init__(self):
        self.session = MysqlUtil().get_session()

    def get_articles(self, page=0, size=20):
        article_num = self.get_article_num()
        if page * size > article_num:
            return None, u'分页数超出最大值'
        info = u'more' if (page + 1) * size < article_num else u'nomore'
        return self.session.query(Article).order_by('id').offset(size * page).limit(size), info

    def get_article_num(self):
        return self.session.query(Article).count()

    def get_article_by_title(self, title):
        return self.session.query(Article).filter(title=title).first()

    def new_article(self, title, author, intro, file_path, tags):
        article = Article(
            title=title,
            intro=intro,
            auth_id=author.id,
            auth_name=author.name,
            filepath=file_path,
            tags=tags
        )


if __name__ == '__main__':
    dao = ArticleDao()
    print dao.get_article_num()
    print dao.get_articles()

