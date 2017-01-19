"""docter server."""

import os
import sys
import mimetypes

from datetime import datetime

from wsgiref import simple_server

import falcon

from jinja2 import Environment, FileSystemLoader


THIS_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def command_stdout(msg):
    sys.stdout.write(msg)


def runserver(app, HOST='127.0.0.1', PORT=5016):
    SETTINGS = 'server.settings'
    httpd = simple_server.make_server(HOST, PORT, app)

    command_stdout('Performing system checks...\n\n')

    now = datetime.now().strftime('%B %d, %Y - %X')
    command_stdout(now)
    command_stdout((
        '\nSystem check identified no issues (0 silenced).\n'
        "Owl version 1.0, using settings '{settings}'\n"
        'Starting development server at http://{addr}:{port}/\n'
        'Quit the server with CONTROL-C.\n'
    ).format(
        port=PORT,
        addr=HOST,
        settings=SETTINGS
    ))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        sys.exit(1)


def handle_404(req, resp):
    resp.status = falcon.HTTP_404
    resp.body = '404'


STATIC_ROOT = os.path.join(BASE_DIR, 'docter/static')

STATIC_URL = '/static/'


def handle_static(req, resp):
    filepath = req.url.split(STATIC_URL)[-1]

    filename = os.path.join(STATIC_ROOT, filepath)

    if not os.path.exists(filename):
        raise falcon.HTTPNotFound()

    with open(os.path.abspath(filename), 'rb') as filehandler:
        filedata = filehandler.read()

    if not filedata:
        return

    content_type, _ = mimetypes.guess_type(req.url)
    resp.content_type = content_type
    resp.body = filedata


class HomePage(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'

        env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)

        with open('demo.md') as file:
            content = file.read()
        # content = content.replace('\n', '\\n"\n+\n"')

        data = env.get_template('demo.html').render(content=content)

        resp.body = data


APP = falcon.API()
APP.add_sink(handle_404)
APP.add_sink(handle_static, prefix='/static')

APP.add_route('/', HomePage())

if __name__ == '__main__':
    runserver(APP)
