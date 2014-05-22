# coding: utf8
import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Numeric,
    DateTime,
    String,
    ForeignKey)
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship)
from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

# Base = declarative_base()
# engine = create_engine('sqlite:///gen_tree.db')
# DBSession.configure(bind=engine)
# Base.metadata.bind = engine
# Base.metadata.create_all(engine)


# def get_base():
#     return Base
#
#
# def get_db_session():
#     return DBSession()
#
#
# def get_engine():
#     return engine


class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    category = Column(Text)
    description = Column(Text)
    rating = Column(Numeric(1,2), default=0)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete='SET NULL'))

    def ideaValidation(self):
        message = list()
        if not self.name:
            message.append(u"Введите название идеи")
        if not self.category:
            message.append(u"Выберите категорию или введите свою")
        if not self.description:
            message.append(u"Напишите описание вашей идеи")
        return message if message else None

    @classmethod
    def addNew(cls, request):
        user = 'user' in request.session and request.session['user']
        if user:
            category = 'newCategory' in request.POST and request.POST['newCategory']
            category = category or ('category' in request.POST and request.POST['category'])
            idea = Idea(
                name='ideasName' in request.POST and request.POST['ideasName'],
                category=category,
                description='description' in request.POST and request.POST['description']
            )
            message = idea.ideaValidation()
            if not message:
                message = [u"Идея добавлена"]
                idea.user = user
                DBSession.add(idea)
                DBSession.flush()
            return message
        else:
            return [u"Чтобы добавить идею нужно войти"]

    @classmethod
    def getCategories(cls):
        all_ideas = cls.allIdeas()
        categories = list()
        for idea in all_ideas:
            if idea.category and not idea.category in categories:
                categories.append(idea.category)
        return categories

    @classmethod
    def allIdeas(cls):
        return DBSession.query(Idea).all()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userName = Column(Text)
    password = Column(Text)
    # relations
    ideas = relationship('Idea', order_by="Idea.id", backref="user")

    def userValidation(self):
        message = list()
        if not self.userName:
            message.append(u"Введите имя пользователя")
        if not self.password:
            message.append(u"Введите пароль")
        if len(DBSession.query(User).filter(User.userName == self.userName).all()):
            message.append(u"Пользователь с таким ником есть")
        return message if message else None

    @classmethod
    def registration(cls, request):
        user = User(userName=request.POST["userName"], password=request.POST["password"])
        message = user.userValidation()
        if not message:
            message = [u"Пользователь зарегистрирован"]
            DBSession.add(user)
            DBSession.flush()
        return message

    @classmethod
    def login(cls, request):
        try:
            user = DBSession.query(User).filter(User.userName == request.POST["userName"]).one()
        except NoResultFound:
            return u"Такой пользователь не зарегистрирован"

        if not user.password == request.POST["password"]:
            return u"Неверное имя пользователя или пароль"
        request.session["user"] = user

    @classmethod
    def logout(cls, request):
        if 'user' in request.session:
            del request.session['user']

