from fs.security import verify
from fs.server import Server
from twisted.internet import reactor
from twisted.python import log
from twisted.web.resource import Resource
from twisted.web.server import Site
import os
import sys

log.startLogging(sys.stdout)

keys = {
    'key1': 'secret1',
    'key2': 'secret2',
    'key3': 'secret3',
    'key4': 'secret4',
}

class AuthView(Resource):
    isLeaf = True

    def __init__(self, keys):
        self.keys = keys
        Resource.__init__(self)
        
    def render_GET(self, request):
        access_id = request.getHeader('djeesefs-access-id')
        signature = request.getHeader('djeesefs-signature')
        print request.args
        if access_id not in self.keys:
            request.setResponseCode(403)
            return ''
        key = self.keys[access_id]
        data = dict((k, v[0]) for k,v in request.args.items())
        if not verify(key, signature, data):
            request.setResponseCode(403)
            return ''
        return ''


class AuthServer(Site):
    def __init__(self, keys):
        Site.__init__(self, AuthView(keys))


oneMB = 1 * 1024 * 1024
tenKB = 10 * 1024
root_path = os.path.abspath('root/')
root_url = 'http://127.0.0.1:9000/content'
auth_server_url = 'http://127.0.0.1:9001'
print '''starting debug server
root: %s
content root: %s
auth server: %s
auth server keys: %s
''' % (root_path, root_url, auth_server_url, keys)
server = Server(root_path, root_url, auth_server_url, oneMB*10, oneMB)
auth = AuthServer(keys)
reactor.listenTCP(9000, server)
reactor.listenTCP(9001, auth)
reactor.run()
