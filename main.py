from Apis.ClientApi import *
from Apis.AdminApi import *
from Apis.UserApi import *
from gevent import pywsgi

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app)
    server.serve_forever()
