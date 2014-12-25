# -*- coding: utf-8 -*-
import json
import os
from twisted.web import static
from twisted.web import resource
from jinja2 import Environment
from jinja2 import FileSystemLoader


def get_package_path():
    return os.path.dirname(os.path.abspath(__file__))

def render_to_response(request, template, context={}):
    path = os.path.join(get_package_path(), 'templates')
    loader = FileSystemLoader(path)
    env = Environment(loader=loader)
    temp = env.get_template(template)
    html = temp.render(context)

    charset = 'utf-8'
    request.setHeader('content-type', 'text/html; charset=%s' % charset)
    return html.encode(charset)

class Root(resource.Resource):
    def __init__(self):
        resource.Resource.__init__(self)

        self.putChild('', Home(self))
        self.putChild('game.html', JsonView(self))

        fp = os.path.join(get_package_path(), 'static')
        self.putChild('static', static.File(fp))

    def getChild(self, name, request):
        return resource.ErrorPage(404, '404', 'Not found')

class Home(resource.Resource):

    def __init__(self, root):
        self.root = root

    def render_GET(self, request):
        return render_to_response(request, 'index.html')

class JsonView(resource.Resource):
    def __init__(self, root):
        self.root = root

    def render_GET(self, request):
        return render_to_response(request, 'game.html')
        # dct = {
        #     'files': "smth",
        # }
        # return json.dumps(dct)