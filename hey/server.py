from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

try:
    from Queue import Queue, Empty
except ImportError:
    # python 3.x
    from queue import Queue, Empty


class HeyQueueFactory(protocol.Factory, object):
    def __init__(self, outQueue, *args, **kwargs):
        self.outQueue = outQueue
        super(HeyQueueFactory, self).__init__(*args, **kwargs)

    def buildProtocol(self, addr):
        return HeyQueueProtocol(self.outQueue)


class HeyQueueProtocol(protocol.Protocol, object):
    def __init__(self, outQueue, *args, **kwargs):
        self.outQueue = outQueue
        super(HeyQueueProtocol, self).__init__(*args, **kwargs)

    def dataReceived(self, data):
        try:
            output = self.outQueue.get_nowait()
        except Empty:
            output = "nothing to report, sir"

        self.transport.write(output)


class HeyProcessProtocol(protocol.ProcessProtocol, object):
    def __init__(self, outQueue, *args, **kwargs):
        self.outQueue = outQueue
        self.status = 'open'
        super(HeyProcessProtocol, self).__init__(*args, **kwargs)

    def outReceived(self, data):
        self.outQueue.put(data)

    def processExited(self, reason):
        self.status = 'closed'

    def processEnded(self, reason):
        self.status = 'closed'
        reactor.stop()


class HeyServer(object):
    def __init__(self, command, port):
        outQueue = Queue()
        self.proc = HeyProcessProtocol(outQueue)
        reactor.spawnProcess(self.proc, command[0], command, usePTY=True)
        endpoint = TCP4ServerEndpoint(reactor, port)
        endpoint.listen(HeyQueueFactory(outQueue))

    def run(self):
        reactor.run()


def start(command):
    host, port = "localhost", 9999

    server = HeyServer(command, port)
    server.run()
