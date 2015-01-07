__author__ = 'frankegoesdown'

from sqlalchemy import *
from time import gmtime, strftime
db = create_engine('sqlite:///base.sqlite')
connection = db.connect()

class SqlCommands:

    def add_user(self, login, password):
        sql = "INSERT INTO users (login, password) VALUES ('{0}', '{1}');".format(login,password)
        connection.execute(sql)

    def create_game(self,user1,user2, date_start):
        sql = "INSERT INTO history_games (user1, user2, date_start) VALUES ('{0}', '{1}', '{2}');".format(user1,user2, date_start)
        connection.execute(sql)

    def user_join(self, user, date):
        sql = "INSERT INTO log_connections (user, date) VALUES ('{0}', '{1}');".format(user, date)
        connection.execute(sql)

    def add_move(self, game, user, from_x, from_y, to_x, to_y):
        sql = ("INSERT INTO moves_log (game_id, user_id, x_start, y_start, x_finish, y_finish)\n"
               "        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}');"
        ).format(game, user, from_x, from_y, to_x, to_y)
        connection.execute(sql)

if __name__ == '__main__':
    c = SqlCommands()
    #c.add_user('user','1234')
    #c.create_game('1','2',strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    #print strftime("%Y-%m-%d %H:%M:%S", gmtime())
