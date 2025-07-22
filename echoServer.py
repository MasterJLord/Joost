# https://stackoverflow.com/questions/7749341/basic-python-client-socket-example

from connectorTester import *

connection = serverConnector(("localhost", 20422), True, 4)
testServerConnector(connection)