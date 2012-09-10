from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import multiprocessing
import types
import __builtin__


POLL_INTERVAL = 0.1


def start_xml_server(port):
    # Create server
    server = SimpleXMLRPCServer(("localhost", port))
    server.register_introspection_functions()
    server.logRequests = 0

    # Register all builtin functions in the xml server:

    for builtin_name in dir(__builtin__):
        if builtin_name is 'print':
            continue
        try:
            func = eval(builtin_name)
            if isinstance(func, types.BuiltinFunctionType):
                server.register_function(func, builtin_name)
        except Exception, e:
            print '*****Failed to eval %s, error = %s' % (builtin_name, e)

    # Run the server's main loop
    server.serve_forever()


class _XMLRPCManager(object):
    '''
    Represents a distributed pythonect server.
    Supports XML-RPCs.
    '''

    def __init__(self, server_name=None, port=8092):

        #Doesn't work, even here. Where does __builtins__ get corrupted?

        if server_name:
            try:
                # TODO: how do we verify that the server exists and is reachable?
                self.server = 'external'
                self.client = xmlrpclib.ServerProxy(server_name)
            except Exception, e:
                print 'Server name %s unsuported, exiting' % server_name
                exit(1)

        else:
            print '==== Starting Pythonect development server ===='
            self.server = self.__start_server_process(port)
            self.client = xmlrpclib.ServerProxy('http://localhost:%d' % port)
            print 'Testing server: max(3,4) = %d' % self.client.max(3, 4)
            print 'Testing server: pow(2,8) = %d' % self.client.pow(2, 8)

    def __start_server_process(self, port):
        '''
        Start xml-rpc server in a new process.
        '''
        proc = multiprocessing.Process(target=start_xml_server, args=(port,))
        proc.start()
        print 'proc', proc
        return proc
