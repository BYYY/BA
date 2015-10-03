__author__ = 'Sapocaly'

from SimpleXMLRPCServer import SimpleXMLRPCServer
import Queue
import utils.PathHelper

Q = Queue.Queue()
S = set()

def save():
    import src.DB.Entry as Entry
    import src.DB.DAL as DAL
    config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                          ['127.0.0.1', 'root', '192519251925', 'ba']))
    global Q
    DAL.create_engine(**config_args)
    with DAL.connection():
        while not Q.empty():
            u = Q.get()
            t = Entry.Url(url=u)
            Entry.Url.add(t)
            del(t)
    print 'all saved!!!!!!!!!!!!!!!!'


def put(url):
    try:
        global Q, S
        if not (url in S):
            Q.put(url)
            S.add(url)
            print url
        return True
    except Exception:
        return False

def get():
    try:
        global Q
        return Q.get()
    except Exception:
        return False


server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_multicall_functions()
server.register_function(put, 'put')
server.register_function(get, 'get')
server.register_function(save, 'save')
server.serve_forever()
