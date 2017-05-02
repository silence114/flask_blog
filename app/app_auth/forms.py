#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
    username = StringField(u'昵称', validators=[DataRequired(), Length(4, 64)])
    password = PasswordField(u'密码', validators=[DataRequired(), Length(4, 64)])
    re_password = PasswordField(u'密码确认', validators=[DataRequired(), Length(4, 64)])
    email = StringField(u'电子邮箱', validators=[DataRequired(), Length(4, 64), Email()])
    remember_me = BooleanField(u'保持登录')
    submit = SubmitField(u'登录')
