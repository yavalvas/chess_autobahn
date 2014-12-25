# -*- coding: utf-8 -*-
from autobahn.twisted.websocket import WebSocketServerFactory, \
     WebSocketServerProtocol, listenWS
import json, cgi

class BroadcastServerProtocol(WebSocketServerProtocol):
    """
    Протокол сервера
    """

    def onOpen(self):
        """
        При открытии вебсокета регистрируем текущий протокол
        :return:
        """
        self.factory.register(self)
    def onMessage(self, payload, isBinary):
        """
        Событие срабатывает при socket.send со стороны клиента
        :param payload:
        :param isBinary:
        :return:
        """
        #парсит json-строку в словарь
        data = json.loads(payload)
        #разбираем различные ситуации. можно переделать в отдельные сервисы на autobahn-е.
        #с запросами на различные url-ы
        if 'username' in data:
            #значит пришла инфа о новом юзере, обрабатываем
            #добавляем в список юзверей
            self.factory.new_user(self, data['username'])
        elif 'create_game' in data:
            #приходит инфа о создании игры
            self.factory.create_game(self, data['create_game'])
        elif 'refresh_game_list' in data:
            #обновляем список доступных игр
            self.factory.send_game_list(self)
    def connectionLost(self, reason):
        """
        При аварийном завершении коннекта
        :param reason:
        :return:
        """
        #проверяется список приконекченных клиентов,
        #каждый клиент - одна вкладка
        if self.factory.clients[self] != '':
            #если не пуст список
            #json с новым списком клиентов и инфой, что один отдисконнектился
            disconnect_msg = json.dumps({'user_disconnect':
                                         self.factory.clients[self]})
            #возвращаем инфу клиенту о дисконекте
            self.factory.broadcast(disconnect_msg, self)
        #удаляем объект, чистим следы
        self.factory.remove_game(self)
        self.factory.unregister(self)
        #посылаем общее сообщение, что коннект завершен с причиной
        WebSocketServerProtocol.connectionLost(self, reason)

class BroadcastServerFactory(WebSocketServerFactory):
    """
    Для обмена сообщениями с клиентом
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug,
                                        debugCodePaths=debugCodePaths)
        self.clients = {}
        self.games = {}
    def register(self, client):
        #новый клиент не среди существующих (клиент как ip)
        if not client in self.clients:
            self.clients[client] = ''
    def unregister(self, client):
        if client in self.clients:
            del self.clients[client]
    def new_user(self, client, username):
        """
        Регистрируем нового юзверя
        :param client:
        :param username:
        :return:
        """
        if len(username) < 3:
            #длина имени слишком короткая
            error = json.dumps({'username_error': 'Username should be at least'
            '3 characters long'})
            #шлём назад клиенту
            client.sendMessage(error)
        #если пользователь уже существует
        elif username in self.clients.itervalues():
            error = json.dumps({'username_error': 'Username already in use'})
            client.sendMessage(error)
        #если всё ок
        else:
            #сохраняем имя пользователя
            #можно прикрутить бд и хранить результаты всех юзеров
            self.clients[client] = username

            #шлём клиента с принятым именем
            accept = json.dumps({'username': username})
            client.sendMessage(accept)

            #шлём список всех текущих юзеров юзеру
            users_list = json.dumps({'users_list': filter(lambda a: a!= '',
                                     self.clients.values())})
            client.sendMessage(users_list)

            #шлём список текущих игр
            self.send_game_list(client)

            #сообщаем каждому о новом пользователе
            new_user = json.dumps({'new_user': username})
            self.broadcast(new_user, client)
    def create_game(self, client, game_settings):
        """
        Проверки при создании игры
        """
        #проверка ошибок при создании игры
        errors = {'numberOfPlayers': [], 'broadSize': [], 'winLength': []}

        if not 2 <= game_settings['numberOfPlayers'] <= 4:
            errors['numberOfPlayers'].append('Must be from 2 to 4')
        if not 2 <= game_settings['boardSize'] <= 10:
            errors['boardSize'].append('Must be from 2 to 10')

        if game_settings['winLength'] < 3:
            errors['winLength'].append('Must be at least 3')

        if game_settings['winLength'] > game_settings['boardSize']:
            errors['winLength'].append('Must be equal or less than board size')

        # silent break when game created with other owner than self
        if game_settings['owner'] != self.clients[client]:
            return
        total_errors = 0
        for key in errors:
            total_errors += len(errors[key])

        if total_errors > 0:
            client.sendMessage(json.dumps({'create_game_error': errors}))
        else:
            self.games[self.clients[client]] = game_settings
            client.sendMessage(json.dumps({'create_game': game_settings}))

    def remove_game(self, client):
        username = self.clients[client]

        if username in self.games:
            del self.games[username]

    def send_game_list(self, client):
        game_list = json.dumps({'game_list': self.games})
        client.sendMessage(game_list)

    def broadcast(self, msg, skip=None):
        for client in self.clients:
            if client != skip and self.clients[client] != '':
                client.sendMessage(msg)
