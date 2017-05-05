#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import login_required
from flask_login import current_user
from . import admin
from flask import flash, redirect, url_for, render_template, request
from models.cate_dao import CategoryDAO
from models.article_dao import ArticleDao


@admin.route('/index')
@admin.route('/')
@login_required
def index():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        return render_template('admin/index.html')


@admin.route('/category')
@login_required
def category():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        from models.cate_dao import CategoryDAO
        cate = CategoryDAO().get_categories()
        return render_template('admin/category.html', categories=cate)


@admin.route('/category/add',methods=['POST'])
@login_required
def category_add():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        cate = request.form.get('cate_name')
        cate_dao = CategoryDAO()
        result, info = cate_dao.add_category(cate)
        cate = cate_dao.get_categories()
        return render_template('admin/category.html', categories=cate, info=info)


@admin.route('/category/delete', methods=['POST'])
@login_required
def category_delete():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        cate_id = request.form.get('cate_id')
        cate_dao = CategoryDAO()
        result, info = cate_dao.delete_category(cate_id)
        cate = cate_dao.get_categories()
        return render_template('admin/category.html', categories=cate, info=info)


@admin.route('/category/update', methods=['POST'])
@login_required
def category_update():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        cate_id = request.form.get('cate_id')
        cate_name = request.form.get('cate_name')

        cate_dao = CategoryDAO()
        result, info = cate_dao.update_category(cate_id, cate_name)
        cate = cate_dao.get_categories()
        return render_template('admin/category.html', categories=cate, info=info)


@admin.route('/article')
@login_required
def article():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        articles, info = ArticleDao().get_articles()
        categories = CategoryDAO().get_categories()
        print categories
        return render_template('admin/article.html', articles=articles, categories=categories)


@admin.route('/article/add', methods=['POST'])
@login_required
def article_add():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        f = request.files['article']
        f.save(u'blogs/{file}'.format(file=f.filename))

        title = request.form.get('art_title')
        art_author = request.form.get('art_author')
        author_id = art_author.split('--')[0] if art_author is not None else 1
        author_name = art_author.split('--')[1] if art_author is not None else 'admin'
        intro = request.form.get('art_intro')
        tags = request.form.get('art_tags')

        result, info = ArticleDao().new_article(title=title,
                                                intro=intro,
                                                author_id=author_id,
                                                author_name=author_name,
                                                filepath=u'blogs/{file}'.format(file=f.filename),
                                                tags=tags
                                                )

        articles, info1 = ArticleDao().get_articles()
        categories = CategoryDAO().get_categories()
        return render_template('admin/article.html', articles=articles, categories=categories, info=info)
        # title = request.form['art_title']
        # title = request.form['art_title']
        # title = request.form['art_title']
        #
        #
        # pattern = re.compile(u'，|,')
        # tags = pattern.split(request.form['tags'])
        # title = request.form['title']
        # author = request.form['author']
        # intro = request.form['intro']
        # is_public = request.form['is_public']
        # category = request.form['category']
        # print 'debug info2'
        # article_id = save_article(title, author, intro, is_public, f.filename, category)
        # print 'debug info3'
        # tag_ids = []
        # for tag in tags:
        #     tag_ids.append(save_tag(tag))
        # print 'debug info4'
        # save_tag_article_relation(article_id, tag_ids)
        # print 'debug info5'
        #
        # # print 'debug info6'
        return '上传成功!'


@admin.route('/account')
@login_required
def account():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        return render_template('admin/account.html')

















































