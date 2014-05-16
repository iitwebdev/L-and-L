import datetime
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Numeric,
    DateTime,
    String,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    name = Column(Text)
    category = Column(Text)
    description = Column(Text)
    rating = Column(Numeric(1,2))
    date = Column(DateTime)
    avtr = Column(String(26))