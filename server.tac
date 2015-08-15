# -*- coding: utf-8 -*-

"""Установки twisted приложения"""

from twisted.internet import reactor
from orm import exceptions
from apps.web import constants

print "-" * 79
print "\tStarting chess_server version %d.%d%s%d" % constants.VERSION_TUPLE
print "-" * 79

reactor.callWhenRunning(exceptions.debug, "\tLoading classes and applications")

# Инициализируем сервер Twisted

import chess_server
chess_server.setUp()

reactor.callWhenRunning(exceptions.debug, "-" * 40)
reactor.callWhenRunning(exceptions.debug, "\tchess_server up and running")

reactor.callWhenRunning(exceptions.debug, "-" * 40)

# Приложение Twisted

application = chess_server.application
