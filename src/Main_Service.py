import flask
import logging
#Added cherrypy as WSGI server
import cherrypy
from paste.translogger import translogger
import json
import numpy as np
import time
import pandas as pd
import os
from random import randint

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
logging.info("Working directory : %s"%(os.getcwd()))
app = flask.Flask(__name__)

@app.route('/rest', methods=['POST'])
def predict():
    data = {"success": False}
    logging.info('Input data___')
    params = flask.request.get_json(force=True)
    logging.info(params)
    score = randint(0,9)
    return flask.jsonify(score)


def run_server():
    #Enable custom paste access logging
    logging.info('Starting____')
    log.format(
        '[%(time)s] REQUEST %(REQUEST_METHOD)s %(status)s %(REQUEST_URI)s '
        '(%(REMOTE_ADDR)s) %(bytes)s'
    )

    app_logged = FotsTransLogger(app, format=log_format)
    #Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged,'/')

    #Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload_on':True,
        'log.screen':True,
        'server.socket_port':5000,
        'server.socket_host':'0.0.0.0'
    })

    #start the server
    cherrypy.engine.start()
    cherrypy.engine.block()

class FotsTransLogger(Translogger):
    #logs activities of API service
    def write_log(self, environ, method, req_uri, start, status, bytes):
        if bytes is None:
            bytes = '-'
        remote_addr = '-'
        if environ.get('HTTP_X_FORWARDED_FOR'):
            remote_addr = environ['HTTP_X_FORWARDED_FOR']
        elif environ.get('REMOTE_ADDR'):
            remote_addr = environ['REMOTE_ADDR']
        d = {
            'REMOTE_ADDR' : remote_addr,
            'REMOTE_USER' : environ.get('REMOTE_USER') or '-',
            'REMOTE_METHOD' : method,
            'REQUEST_URI' : req_uri,
            'HTTP_VERSION' : environ.get('SERVER_PROTOCOL'),
            'time' : time.strftime('%d/%b/%Y:%H:%M:%S', start),
            'status' : status.split(None, 1)[0],
            'bytes':bytes,
            'HTTP_REFERER' : environ.get('HTTP_REFERER','-'),
            'HTTP_USER_AGENT' : environ.get('HTTP_USER_AGENT','-'),
        }

        message = self.format % d
        self.logger.log(self.logging_level, message)

#start flask app

if __name__ == "__main__":
    logging.info(("Flask starting server..."
        "please wait until  server has fully started"))
    run_server()

