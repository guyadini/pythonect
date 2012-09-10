from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import multiprocessing


POLL_INTERVAL = 0.1

def start_xml_server(port):
    # Create server
    server = SimpleXMLRPCServer(("localhost", port) )
    server.register_introspection_functions()
    
    # Register all builtin functions in the xml server:
    
    ######################################
    # How do I get to __builtin__?
    print dir()
    print dir(__builtin__)
    #################################
    
    
    exit(1)
    for builtin_name in dir(__builtin__):
        try:
            func = eval(builtin_name)
            server.register_function(func, builtin_name)
            print 'registered %s successfully' % builtin_name
        except Exception, e:
            print '*****Failed to eval %s' % builtin_name
        
    
    # Run the server's main loop
    server.serve_forever()
    



class _DistServer(object):
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
            print 'Methods: ', self.client.system.listMehods()
            print 'Testing server: max(3,4) = %d' % self.client.max(3,4)

        
    def __start_server_process(self, port):
        '''
        Start xml-rpc server in a new process.
        '''
        proc = multiprocessing.Process(target=start_xml_server, args=(port,))
        proc.start()
        
        

        
