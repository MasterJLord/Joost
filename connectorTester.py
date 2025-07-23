import random
from socketThread import serverConnector

def testServerConnector(connector : serverConnector):
    connector.sendInt(connector.myPlayerNum)
    connector.sendInt(random.randint(10, 99))
    connector.sendInt(random.randint(10000,99999))
    for i in range(9):
        print(connector.getInt(connector.getNextSender()))
        