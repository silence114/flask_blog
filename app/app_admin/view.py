#!/usr/bin/python
# -*- coding:utf-8 -*-
from flask_login import login_required
from flask_login import current_user
from . import admin
from flask import flash, redirect, url_for, render_template, request
from models.cate_dao import CategoryDAO
from models.article_dao import ArticleDao
from models.author_dao import AuthorDAO


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


@admin.route('/category/add', methods=['POST'])
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
        authors = AuthorDAO().get_authors()
        return render_template('admin/article.html', articles=articles, categories=categories, authors=authors)


@admin.route('/article/delete', methods=['POST'])
@login_required
def article_delete():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        art_id = request.form.get('art_id')
        art_dao = ArticleDao()
        article = art_dao.get_article_by_id(art_id)
        if article is not None:
            result, info = art_dao.delete_article(article)
        else:
            info = u'要删除的文章ID不存在!'

        articles, info1 = art_dao.get_articles()
        categories = CategoryDAO().get_categories()
        authors = AuthorDAO().get_authors()
        return render_template('admin/article.html', articles=articles, categories=categories, authors=authors, info=info)


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
        author_name = art_author.split('--')[1] if art_author is not None else u'admin'
        category = request.form.get('art_cate')
        cate_id = category.split('--')[0] if category is not None else 1
        cate_name = category.split('--')[1] if category is not None else u'未分类'
        intro = request.form.get('art_intro')
        tags = request.form.get('art_tags')
        tags = tags.replace(u'，', ',')

        result, info = ArticleDao().new_article(title=title,
                                                intro=intro,
                                                author_id=author_id,
                                                author_name=author_name,
                                                cate_id=cate_id,
                                                cate_name=cate_name,
                                                filepath=u'blogs/{file}'.format(file=f.filename),
                                                tags=tags
                                                )
        articles, info1 = ArticleDao().get_articles()
        categories = CategoryDAO().get_categories()
        authors = AuthorDAO().get_authors()
        return render_template('admin/article.html', articles=articles, categories=categories, authors=authors, info=info)


@admin.route('/account')
@login_required
def account():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        authors = AuthorDAO().get_authors()
        return render_template('admin/account.html', authors=authors)


@admin.route('/account/add', methods=['POST'])
@login_required
def account_add():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        author_name = request.form.get('author_name')
        auth_dao = AuthorDAO()
        result, info = auth_dao.add_author(author_name)
        authors = auth_dao.get_authors()
        return render_template('admin/account.html', authors=authors, info=info)


@admin.route('/account/delete', methods=['POST'])
@login_required
def account_delete():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        author_name = request.form.get('author_name')
        auth_dao = AuthorDAO()
        result, info = auth_dao.delete_author(author_name)
        authors = auth_dao.get_authors()
        return render_template('admin/account.html', authors=authors, info=info)


@admin.route('/account/update', methods=['POST'])
@login_required
def account_update():
    if current_user.is_admin == 0:
        flash(u'只有管理员才有权限查看当前页面!')
        return redirect(url_for('main.index'))
    else:
        author_name = request.form.get('author_name')
        auth_dao = AuthorDAO()
        author = auth_dao.get_author_by_name(author_name)
        if author is not None:
            info = u'修改失败,作者名已近存在!'
        else:
            author_id = request.form.get('author_id')
            result, info = auth_dao.update_author(author_id, author_name)
        authors = auth_dao.get_authors()
        return render_template('admin/account.html', authors=authors, info=info)
