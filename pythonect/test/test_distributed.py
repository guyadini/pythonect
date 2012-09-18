#!/usr/bin/python

try:

    # If < Python 2.7, use the backported unittest2 package

    import unittest2 as unittest

except ImportError:

    # Probably > Python 2.7, use unittest

    import unittest

import os
import sys


# Local imports

import pythonect


#TODO - this should run first but it doesn't. Figure it out.
def setUpModule():
    print '>>>>>>>>>> Entering distributed setupModule'
    global rpc_manager
    rpc_manager = pythonect._XMLRPCManager()




class TestPythonectDistributed(unittest.TestCase):
    print '>>>>>>>>>> Entering distributed test'


