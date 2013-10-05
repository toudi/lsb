#!/bin/env/python

from ConfigParser import SafeConfigParser
import socket
from random import choice
from json import dumps


config = SafeConfigParser()
config.read('conf/client.conf')

available_scout_hosts = config.get('lsb', 'scouts').split(',')
random_scout_socket = choice(available_scout_hosts).split(':')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((random_scout_socket[0], int(random_scout_socket[1])))

job = {
    'worker': 'foo.bar',
    'method': 'helloworld',
    'args': [],
    'kwargs': {'foo': 'bar'}
}

s.sendall(dumps(job)+"\n")

response = s.recv(4096)

print("Got a result", response)

s.close()