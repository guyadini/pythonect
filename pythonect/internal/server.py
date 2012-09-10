from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib


POLL_INTERVAL = 0.1


class _DistServer(object):
    '''
    Represents a distributed pythonect server.
    Supports XML-RPCs.
    '''

    def __init__(self, server_name=None, port=8092):
        if server_name:
            try:
                self.server = SimpleXMLRPCServer(server_name)
            except Exception, e:
                print 'Server name %s unsuported, exiting' % server_name
                exit(1)

        else:
            print '==== Starting Pythonect development server ===='
            self.server = __start_server_process(port)

        #TODO: register functions

        self.server.serve_forever(poll_interval=POLL_INTERVAL)

    # TODO - implement, wrap all python builtins. Cool!

    def __start_server_process(self, port):
        '''
        Start xml-rpc server in a new process.
        '''

        raise Exception('TODO: implement, i.e. http://docs.python.org/library/simplexmlrpcserver.html#SimpleXMLRPCServer.CGIXMLRPCRequestHandler')
