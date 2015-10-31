import utils.PathHelper

utils.PathHelper.configure_dir()

from SimpleXMLRPCServer import SimpleXMLRPCServer


def log():
    """
    a centralized log service
    """
    pass


if __name__ == '__main__':
    server = SimpleXMLRPCServer(("127.0.0.1", 8001))
    print "starting service......"
    server.register_multicall_functions()
    server.register_function(log, 'log')
    print 'ready for service "save"'
    server.serve_forever()
