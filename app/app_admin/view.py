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


@admin.route('/account')
@login_required
def account():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        return render_template('admin/account.html')
