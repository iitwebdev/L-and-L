#coding: utf-8
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    return {'project': 'MyProject1'}

@view_config(route_name='page', renderer='templates/page.jinja2')
def page_view(request):
    return {'project': 'MyProject1'}

@view_config(route_name='user', renderer='templates/user.jinja2')
def user_view(request):
    return {'project': 'MyProject1'}