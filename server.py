#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
import json
from bottle import request, run, get, post

# app config
app_config_path = '/etc/bsp_server.json'
password = None
if not os.path.exists(app_config_path):
    import uuid
    password = str(uuid.uuid4())[-10:-1]
    config = {
        "password" : password
    }
    with codecs.open(app_config_path, 'w', 'utf-8') as json_file:
        json_file.write(json.dumps(config, sort_keys=True, indent=4).decode('utf-8'))
else:
    with codecs.open(app_config_path) as json_file:
        data = json.load(json_file)
        password = data.get('password',None)
    if not password:
        password = str(uuid.uuid4())[-10:-1]
        config = {
            "password" : password
        }
        with codecs.open(app_config_path, 'w', 'utf-8') as json_file:
            json_file.write(json.dumps(config, sort_keys=True, indent=4).decode('utf-8'))

print "password:",password

def check_auth():
    key = request.params.get('key',None)
    return (key == password)

@post('/ping')
def ping():
    if not check_auth():
        return 'no auth'
    return "pong"

@post('/create')
def create():
    if not check_auth():
        return 'no auth'

    port = request.params.get('port',None)
    password = request.params.get('password',None)
    bandwith = request.params.get('bandwith',None)
    if not port or not password or not bandwith:
        return 'argument error'
    try:
        port = int(port)
        bandwith = int(bandwith)
    except Exception as e:
        return 'argument error'

    if bandwith < 0 or bandwith > 200 * 1000:
        return 'bandwith error'

    cmd = 'bsp -p %d -P %s -s %d -a -A -j'%(port,password,bandwith)
    if os.system('bsp ') != 0:
        return 'create 500'
    else:
        return 'create ok'

run(host='0.0.0.0', port=8081,reloader=True)
