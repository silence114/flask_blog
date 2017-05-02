#!/usr/bin/python
# -*- coding:utf-8 -*-
from . import auth
from flask import request, redirect, render_template, flash, url_for
from forms import LoginForm
from flask_login import login_user,logout_user
from models.users_dao import UsersDAO
from models.models import User
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from utils.config_util import ConfigUtil
from flask_login import login_required
from utils.mail_util import MailUtil
import re


@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'GET':
        return render_template('auth/login1.html', login_form=login_form)
    else:
        password = request.form.get('password')
        email = request.form.get('email')
        user_dao = UsersDAO()
        user = user_dao.get_user_by_email(email)
        if user is None:
            return render_template('auth/login1.html', error_msg=u'邮箱账号不存在!')
        else:
            if not check_password_hash(user.password, password):
                return render_template('auth/login1.html', error_msg=u'用户名密码错误!')
            else:
                login_user(user, login_form.remember_me.data)
                return redirect(request.args.get('next') or '/index')


@auth.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash(u'已经退出登录!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/regisiter.html', error_msg=None)
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('re_password')
        education = request.form.get('education')
        interest = request.form.getlist('interest')
        agree = request.form.get('agree')

        print '====>>',username,email,password,repassword,agree

        if not re.compile('^[0-9a-zA-Z]{4,20}$').match(username):
            return render_template('auth/regisiter.html', error_msg=u'昵称为长度4到20的字母、数字、下划线、@、#、$组合')
        if len(password) < 4 or len(password) > 20:
            return render_template('auth/regisiter.html', error_msg=u'密码长度为4到20个字符')
        if password != repassword:
            return render_template('auth/regisiter.html', error_msg=u'两次输入的密码不一致')
        if not re.compile(u'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$').match(email):
            return render_template('auth/regisiter.html', error_msg=u'请输入合法的邮箱地址!')

        user_dao = UsersDAO()
        if user_dao.get_user_by_email(email) is not None:
            return render_template('auth/regisiter.html', error_msg=u'邮箱已经被注册!')

        password_hash = generate_password_hash(password)
        user = User(username=username,
                    password=password_hash,
                    email=email,
                    status=0,
                    register_time=datetime.now(),
                    last_login_time=datetime.now()
                    )
        user_dao.add_user(user)
        MailUtil().send_confirm_mail(username, email)
        render_template('auth/register_comfirm.html')


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    s = Serializer(ConfigUtil().get_config('SECRET_KEY'))
    try:
        email = s.loads(token)
    except:
        return u'确认邮件超时,必须在半小时内确认!'
    print '========>>', email, '<<========'
    user_dao = UsersDAO()
    result, mesg = user_dao.confirm_email(email)
    if result:
        return redirect('/index')
    else:
        return mesg
