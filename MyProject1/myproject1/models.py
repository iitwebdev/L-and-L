# coding: utf8
import datetime

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Numeric,
    DateTime,
    String,
    )
from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from sqlalchemy.orm.exc import NoResultFound

from zope.sqlalchemy import ZopeTransactionExtension
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

Base = declarative_base()
engine = create_engine('sqlite:///gen_tree.db')
DBSession.configure(bind=engine)
Base.metadata.bind = engine
Base.metadata.create_all(engine)


def get_base():
    return Base


def get_db_session():
    return DBSession()


def get_engine():
    return engine


class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    category = Column(Text)
    description = Column(Text)
    rating = Column(Numeric(1,2))
    date = Column(DateTime)
    author = Column(String(26))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    userName = Column(Text)
    password = Column(Text)

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