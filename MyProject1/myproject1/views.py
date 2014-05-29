#coding: utf-8
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .models import DBSession, Idea
from .models import User


def bindUser(fn):
    def wrapped(request):
        if 'user' in request.session:
            DBSession.add(request.session['user'])
        return fn(request)

    return wrapped


@view_config(route_name='home', renderer='templates/home.jinja2')
@bindUser
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
@bindUser
def page_view(request):
    response = {'categories': Idea.getCategories(),
                'all_ideas': Idea.searchIdea(request) if 'search' in request.POST else Idea.allIdeas(),
                'top10': Idea.top10()}
    return response


@view_config(route_name='user', renderer='templates/user.jinja2')
@bindUser
def user_view(request):
    user = 'user' in request.session and request.session['user']
    if user:
        DBSession.add(user)
    response = {'all_ideas': user.ideas if user else []}
    if 'addIdea' in request.POST:
        response["messages"] = Idea.addNew(request)
    response["categories"] = Idea.getCategories()
    return response


@view_config(route_name='logout', renderer='string')
def logout(request):
    try:
        User.logout(request)
    except:
        return "error"
    else:
        return 'OK'


@view_config(route_name='description', renderer='templates/description.jinja2')
@bindUser
def description_view(request):
    if 'back' in request.POST:
        return HTTPFound(location=request.route_url('page'))
    idea_id = 'id' in request.matchdict and request.matchdict['id']
    if idea_id:
        idea = DBSession.query(Idea).get(idea_id)
        if idea:
            user = 'user' in request.session and request.session['user']
            users = idea.users_like
            if 'estimate' in request.POST:
                if 'rating' in request.POST and user and not user in users:
                    rating = int(request.POST['rating'])
                    idea.rating = (idea.rating * len(users) + rating)/(len(users) +1)
                    idea.users_like.append(user)
                    idea.save()

            return {'idea': idea, 'rating': idea.rating if not user or user in users else None}

    return HTTPFound(location=request.route_url('page'))
