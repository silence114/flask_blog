#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from utils.config_util import ConfigUtil

app = Flask(__name__)
conf = ConfigUtil()
app.config['SECRET_KEY'] = conf.get_config('SECRET_KEY')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    from app_auth import auth
    from app_main import main
    from app_admin import admin

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager.init_app(app)
    return app



