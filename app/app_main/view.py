#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import login_required
from flask import render_template
from models.cate_dao import CategoryDAO
from models.article_dao import ArticleDao
from . import main


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
