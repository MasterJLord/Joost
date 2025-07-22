import random
from socketThread import serverConnector

def testServerConnector(connector : serverConnector):
    connector.sendInt(connector.myPlayerNum)
    connector.sendInt(random.randint(10000000000000000000000000000000000000000, 100000000000000000000000000000000000000000000100000000000000000000000000000000000000000000))
    for i in range(8):
        print(connector.getInt(connector.getNextSender()))