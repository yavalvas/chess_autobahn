# -*- coding: utf-8 -*-
__author__ = 'yav'

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# engine = create_engine('postgresql://scott:tiger@localhost/mydatabase')
#TODO: поменять на postgres?
engine = create_engine('sqlite:////tmp/test.db', convert_unicode=True)
#пока база в tmp. Пример из flask-а
#metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
def init_db():
    #TODO: сделать добавление модулей orm из конфига server_settings
    import orm.admin
    Base.metadata.create_all(bind=engine)