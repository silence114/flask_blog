#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import render_template, abort
from models.cate_dao import CategoryDAO
from models.article_dao import ArticleDao
from . import main
import os


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