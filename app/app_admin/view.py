#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import login_required
from flask_login import current_user
from . import admin
from flask import flash, redirect, url_for, render_template


@admin.route('/index')
@login_required
def index():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        return render_template('admin/index.html')