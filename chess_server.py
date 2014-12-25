# -*- coding: utf-8 -*-
import sys
from twisted.web import server
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.application import internet, service
from ws_server import BroadcastServerFactory, BroadcastServerProtocol
from autobahn.twisted.websocket import listenWS
from autobahn.twisted.resource import WebSocketResource, HTTPChannelHixie76Aware

web_root = None
application = service.Application("chess")

def setUp():
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False
    try:
        import autobahn
        import twisted
    except ImportError:
        sys.exit("Install all dependencies")
    from orm.database_init import init_db, db_session
    from apps.web import constants
    init_db()
    from apps.web import main_resource
    root = main_resource.Root()
    reactor.listenTCP(8000, server.Site(main_resource.Root()))
    factory = BroadcastServerFactory("ws://127.0.0.1:8011", debug=debug, debugCodePaths=debug)
    factory.protocol = BroadcastServerProtocol
    factory.setProtocolOptions(allowHixie76=True)
    ws_resource = WebSocketResource(factory)
    root.putChild("ws", ws_resource)
    site = Site(root)
    site.protocol = HTTPChannelHixie76Aware
    listenWS(factory)
    reactor.run()

if __name__=="__main__":
    setUp()