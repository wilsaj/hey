from sys import stdout

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint

debug = False


class HeyProtocol(Protocol):
    def sendMessage(self, message):
        self.transport.write(message)
        if debug:
            stdout.write("Sent:     {}\n".format(message))

    def dataReceived(self, data):
        if debug:
            stdout.write("Received: \n")
        stdout.write(str(data))
        self.transport.loseConnection()
        reactor.stop()


class HeyFactory(Factory):
    def buildProtocol(self, addr):
        return HeyProtocol()


def stopit():
    _send_message('stopit')


def whatsup():
    _send_message('whatsup')


def _build_message_callback(message):
    def protocol_callback(p):
        p.sendMessage(message)

    return protocol_callback


def _send_message(message):
    HOST, PORT = "localhost", 9999

    point = TCP4ClientEndpoint(reactor, HOST, PORT)
    d = point.connect(HeyFactory())
    d.addCallback(_build_message_callback(message))
    reactor.run()
