__author__ = 'Sapocaly'

import utils.PathHelper
utils.PathHelper.configure_dir()

from SimpleXMLRPCServer import SimpleXMLRPCServer
import Queue

import src.DB.Entry as Entry
import src.DB.DAL as DAL


from utils import DBconfig



Q = Queue.Queue()
S = set()

config = DBconfig.DBConfig("conf/byyy_ba_db.cfg")
config_args = dict(zip(['host', 'user', 'passwd', 'database'],
                           [config.DB_HOST, config.DB_USER, config.DB_PASSWORD, config.DB_NAME]))
DAL.create_engine(**config_args)

def save():
    global Q
    with DAL.connection():
        while not Q.empty():
            u = Q.get()
            t = Entry.Url(url=u)
            Entry.Url.add(t)
            del (t)
    print 'all saved!!!!!!!!!!!!!!!!'
    return True


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


# ip 0.0.0.0 for remote usage
server = SimpleXMLRPCServer(("localhost", 8000))
print "Listening on port 8000..."
server.register_multicall_functions()
server.register_function(put, 'put')
server.register_function(get, 'get')
server.register_function(save, 'save')
server.serve_forever()
