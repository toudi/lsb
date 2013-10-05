#!/bin/env python

from ConfigParser import SafeConfigParser
from json import loads
from SocketServer import ThreadingTCPServer, BaseRequestHandler
from importlib import import_module

config = SafeConfigParser()
config.read('conf/scout.conf')

class ScoutServerHandler(BaseRequestHandler):
    @property
    def job_backend_client(self):
        return import_module('backend.%s' % config.get('scout', 'backend')).Backend()
    @property
    def middlewares(self):
        for m in config.get('scout', 'middleware').split(','):
            yield import_module('middleware.%s' % m).Middleware()

    def handle(self):
        data = self.request.recv(1024).strip()
        buffer = data
        while (len(data) == 1024):
            data = self.request.recv(1024).strip()
            buffer += data

        self.request.sendall('OK')
        job = loads(buffer)

        for m in self.middlewares:
            m.process(job)

        print(self.job_backend_client.submit(job))
        # That's all, folks!






socket = config.get('scout', 'socket').split(':')
(host, port) = (socket[0], int(socket[1]))

server = ThreadingTCPServer((host, port), ScoutServerHandler)
server.serve_forever()