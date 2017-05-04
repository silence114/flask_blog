#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import login_required
from flask_login import current_user
from . import admin
from flask import flash, redirect, url_for, render_template, request
from models.cate_dao import CategoryDAO


@admin.route('/index')
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
        return render_template('admin/article.html')


@admin.route('/admin/article/add')
@login_required
def article_add():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        # f = request.files['art_filepath']
        # f.save(u'blogs/{file}'.format(file=f.filename))
        #
        # title = request.form['art_title']
        # art_author = request.form['art_author']
        #
        # author_id = art_author.split('--')[0]
        # author_name = art_author.split('--')[1]
        #
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

















































