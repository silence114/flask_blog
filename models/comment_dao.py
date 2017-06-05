#!/usr/bin/python
# -*- coding:utf-8 -*-

from models import Comment
from utils.mysql_util import MysqlUtil
from article_dao import ArticleDao
from flask_login import current_user
from sqlalchemy import desc


class CommentDAO:
    def __init__(self):
        self.session = MysqlUtil().get_session()

    def new_comment(self, art_id, content):
        if ArticleDao().get_article_by_id(art_id) is None:
            return False, u'评论的文章不存在'
        else:
            comment = Comment()
            comment.article_id = art_id
            comment.comment = content
            comment.user = current_user.username
            self.session.add(comment)
            self.session.commit()
            return True, u'评论成功!'

    def get_article_comments_num(self, art_id):
        return self.session.query(Comment) \
            .filter_by(article_id=art_id).count()

    def get_comments_by_article(self, article_id, page=0, size=20):
        article_num = self.get_article_comments_num(article_id)
        if page * size > article_num:
            return None, u'分页数超出最大值'
        info = u'more' if (page + 1) * size < article_num else u'nomore'
        return self.session.query(Comment)\
                   .filter_by(article_id=article_id)\
                   .order_by(desc(Comment.modified_time)).offset(size * page).limit(size).all(), info


if __name__ == '__main__':
    cd = CommentDAO()
    print cd.get_article_comments_num(5)
    print cd.get_article_comments_num(4)
    print cd.get_comments_by_article(5)
    print cd.get_comments_by_article(4)
