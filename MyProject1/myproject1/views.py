#coding: utf-8
import datetime
from pyramid.response import Response
from pyramid.view import view_config

from pyramid.security import forget

from sqlalchemy.exc import DBAPIError

from .models import DBSession, Idea, Base
from .models import User, get_base, get_db_session, get_engine


@view_config(route_name='home', renderer='templates/home.jinja2')
def my_view(request):
    response = {'userName': ""}
    if 'userName' and 'password' in request.POST:
        response['userName'] = request.POST["userName"]
        if 'register' in request.POST:
            response["messages"] = User.registration(request)
        if 'login' in request.POST:
            m = User.login(request)
            if m:
                response["messages"] = [m]
    return response


@view_config(route_name='page', renderer='templates/page.jinja2')
def page_view(request):
    all_ideas = DBSession.query(Idea).all()
    categories = list()
    for idea in all_ideas:
        if idea.category and not idea.category in categories:
            categories.append(idea.category)
    return {'all_ideas': all_ideas, 'categories': categories}


@view_config(route_name='user', renderer='templates/user.jinja2')
def user_view(request):
    return {'project': 'MyProject1'}

@view_config(route_name='logout', renderer='string')
def logout(request):
    try:
        User.logout(request)
    except:
        return "error"
    else:
        return 'OK'