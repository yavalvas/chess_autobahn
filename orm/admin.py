from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship, backref
from database_init import Base
import datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True)
    password = Column(String(50))
    dateregister = Column(DateTime, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    name = Column(String(50))
    email = Column(String(50), unique=True)

    log_connections = relationship("LogConnections", uselist=False, backref="users")
    user_connections_black = relationship("HistoryGames", primaryjoin="User.id==HistoryGames.black",
                                          uselist=False)
    user_connections_white = relationship("HistoryGames", primaryjoin="User.id==HistoryGames.white",
                                          uselist=False)
    moves_log_rel = relationship("MovesLog", uselist=False, backref="users")
    def __init__(self, login=None, password=None, name=None, email=None, dateregister=None):
        self.name = name
        self.email = email
        self.login = login
        self.password = password
	self.dateregister = datetime.datetime.now()

    def __repr__(self):
        return '<User %r>' % (self.name)

class LogConnections(Base):
    __tablename__ = 'log_connections'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    joined_date = Column(DateTime, onupdate=datetime.datetime.now)
    def __init__(self, user_id=None):
        self.user_id = user_id


class HistoryGames(Base):
    __tablename__ = 'history_games'
    id = Column(Integer, primary_key=True)
    black = Column(Integer, ForeignKey('users.id'))
    white = Column(Integer, ForeignKey('users.id'))
    date_start = Column(DateTime)
    date_finish = Column(DateTime)
    moves_log = relationship("MovesLog", backref="history_games")
    def __init__(self, black=None, white=None, date_start=None,
                 date_finish=None):
        self.black = black
        self.white = white
        self.date_start = date_start
        self.date_finish = date_finish


class MovesLog(Base):
    __tablename__ = 'moves_log'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('history_games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    from_xy = Column(VARCHAR(2))
    to_xy = Column(VARCHAR(2))
    def __init__(self, game_id, user_id, from_xy, to_xy):
        self.game_id = game_id
        self.user_id = user_id
        self.from_xy = from_xy
        self.to_xy = to_xy
