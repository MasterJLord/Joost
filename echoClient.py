from connectorTester import *

connection = serverConnector(("localhost", 20422), False)
testServerConnector(connection)