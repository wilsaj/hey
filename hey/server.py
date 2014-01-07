from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

try:
    from Queue import Queue, Empty
except ImportError:
    # python 3.x
    from queue import Queue, Empty


# yeah, globals are bad and all that
server = None


class HeyQueueFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return HeyQueueProtocol()


class HeyQueueProtocol(protocol.Protocol):
    def dataReceived(self, data):
        global outQueue
        try:
            output = outQueue.get_nowait()
        except Empty:
            output = "nothing to report, sir"

        self.transport.write(output)


class HeyProcessProtocol(protocol.ProcessProtocol, object):
    def __init__(self, *args, **kwargs):
        global outQueue
        outQueue = Queue()
        self.status = 'open'
        super(HeyProcessProtocol, self).__init__(*args, **kwargs)

    def outReceived(self, data):
        global outQueue
        outQueue.put(data)

    def processExited(self, reason):
        self.status = 'closed'

    def processEnded(self, reason):
        self.status = 'closed'
        reactor.stop()


class HeyServer(object):
    def __init__(self, command, port):
        self.proc = HeyProcessProtocol()
        reactor.spawnProcess(self.proc, command[0], command, usePTY=True)
        endpoint = TCP4ServerEndpoint(reactor, port)
        endpoint.listen(HeyQueueFactory())

    def run(self):
        reactor.run()


def start(command):
    global server
    host, port = "localhost", 9999

    server = HeyServer(command, port)
    server.run()
