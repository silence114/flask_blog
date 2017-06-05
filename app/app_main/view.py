#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import render_template, abort, request, redirect
from models.cate_dao import CategoryDAO
from models.article_dao import ArticleDao
from models.comment_dao import CommentDAO
from . import main
import os, json
from flask_login import login_required


@main.route('/')
@main.route('/index')
def index():
    cate_dao = CategoryDAO()
    categories = cate_dao.get_categories()
    articles, more = ArticleDao().get_articles()
    return render_template('main/index.html',
                           categories=categories,
                           articles=articles,
                           more=True if more == 'more' else False)


@main.route('/about_me')
def about_me():
    return render_template('about_me.html')


@main.route('/category/<int:category_id>')
def category(category_id):
    cate_dao = CategoryDAO()
    if cate_dao.get_cate_by_id(category_id) is None:
        abort(404)
    categories = cate_dao.get_categories()

    articles, more = ArticleDao().get_articles_by_cate(category_id)

    return render_template('main/index.html',
                           categories=categories,
                           articles=articles,
                           active_cat=category_id,
                           more=True if more == 'more' else False)


@main.route('/article/<int:article_id>')
def article(article_id):
    categories = CategoryDAO().get_categories()
    article1 = ArticleDao().get_article_by_id(article_id)
    if article1 is None:
        return abort(404)
    return render_template('main/article.html',
                           categories=categories,
                           article_id=article1.id,
                           active_cat=article1.cate_id)


@main.route('/getArticleContext/<int:article_id>')
def get_article_content(article_id):
    try:
        article = ArticleDao().get_article_by_id(article_id)
        if article is None:
            abort(404)

        filename = os.path.sep.join([os.path.dirname(os.path.realpath(__file__)), '..', '..', article.file_path])
        with open(filename) as blog:
            html = '\n'.join(blog.readlines())
        return html
    except IOError:
        abort(500)


@main.route('/comment', methods=['POST'])
@login_required
def comment():
    article_id = request.form['article']
    if ArticleDao().get_article_by_id(article_id) is None:
        abort(404)
    comment = request.form['comment']
    result, info = CommentDAO().new_comment(article_id, comment)
    if result:
        return redirect('/article/{art_id}'.format(art_id=article_id))
    else:
        abort(404)


@main.route('/getArticleComment/<int:article_id>', methods=['POST', 'GET'])
def get_article_comment(article_id):
    article = ArticleDao().get_article_by_id(article_id)
    if article is None:
        abort(404)
    # return json.dumps(
    #     [
    #         {
    #             'user': 'renjie'
    #             , 'create_time': '2017-12-12 12:12:12'
    #             , 'content': '这是测试文章的测试评论,所以评论内容可能一堆你看不懂的东西,这你应该能理解吧~'
    #             , 'good': 10
    #             , 'bad': 0
    #             , 'replay': "renjie,,,2017-12-12 12:12:12,,,这是回复内容"
    #         }, {
    #             'user': 'renjie'
    #             , 'create_time': '2017-12-12 12:12:13'
    #             , 'content': '这是测试文章的测试评论,所以评论内容可能一堆你看不懂的东西,这你应该能理解吧~'
    #             , 'good': 10
    #             , 'bad': 0
    #             , 'replay': "renjie,,,2017-12-12 12:12:13,,,这是回复内容"
    #         }
    #     ]
    # )
    results, info = CommentDAO().get_comments_by_article(article_id)

    comment_list = []
    for comment in results:
        c = {}
        c['id'] = comment.id
        c['article_id'] = comment.article_id
        c['user'] = comment.user
        c['comment'] = comment.comment
        c['good'] = comment.good
        c['bad'] = comment.bad
        c['replay'] = comment.replay
        c['create_time'] = comment.create_time.strftime('%Y-%m-%d %H:%M:%S')
        c['modified_time'] = comment.modified_time.strftime('%Y-%m-%d %H:%M:%S')
        print c
        comment_list.append(c)
    return json.dumps(comment_list)
    # return 'hello'


@main.route('/tag/<string:tag>')
def tags(tag):
    articles, more = ArticleDao().get_article_by_tag(tag)
    categories = CategoryDAO().get_categories()
    return render_template('main/index.html',
                           categories=categories,
                           articles=articles,
                           more=True if more == 'more' else False)


@main.route('/about')
def about():
    return render_template('about.html')

