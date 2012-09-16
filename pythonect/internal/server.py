from SimpleXMLRPCServer import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import SocketServer
import xmlrpclib
import multiprocessing
import types
import __builtin__


ENABLE_SERVER_LOGGING = True


POLL_INTERVAL = 0.1

# TODO: add the option of having the server log all requests, for debugging.


# Taken from http://code.activestate.com/recipes/425043-simple-threaded-xml-rpc-server/
class AsyncXMLRPCServer(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass


# Taken from http://code.activestate.com/recipes/496700-logging-simplexmlrpcserver/
# But without using the logging class (so that the main log isn't touched).
log_file = open('xmlrpc.log', 'w')


class LoggingSimpleXMLRPCRequestHandler(SimpleXMLRPCRequestHandler):
    """Overides the default SimpleXMLRPCRequestHander to support logging.  Logs
    client IP and the XML request and response.
    """

    def do_POST(self):
        clientIP, port = self.client_address
    # Log client IP and Port
        log_file.write('Client IP: %s - Port: %s' % (clientIP, port))
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # Log client request
            log_file.write('Client request: \n%s\n' % data)
            response = self.server._marshaled_dispatch(data, getattr(self, '_dispatch', None))

            # Log server response
            log_file.write('Server response: \n%s\n' % response)
            log_file.flush()

        except:  # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)


def start_xml_server(port):
    '''
    Start an XML-RPC server at the given port.
    '''
    # Create server
    if ENABLE_SERVER_LOGGING is True:
        server = AsyncXMLRPCServer(("localhost", port), requestHandler=LoggingSimpleXMLRPCRequestHandler)
    else:
        server = AsyncXMLRPCServer(("localhost", port))

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
            #print 'Testing server: max(3,4) = %d' % self.client.max(3, 4)
            #print 'Testing server: pow(2,8) = %d' % self.client.pow(2, 8)

    def __start_server_process(self, port):
        '''
        Start xml-rpc server in a new process.
        '''
        proc = multiprocessing.Process(target=start_xml_server, args=(port,))
        proc.start()
        print 'proc', proc
        return proc
