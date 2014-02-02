from twisted.internet import protocol, reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

try:
    from Queue import Queue, Empty
except ImportError:
    # python 3.x
    from queue import Queue, Empty


class ProcessInfo(object):
    """Holds state of a process (including output and status)."""
    outQueue = Queue()
    status = None


class HeyResponderFactory(protocol.Factory, object):
    def __init__(self, process_info, *args, **kwargs):
        self.process_info = process_info
        super(HeyResponderFactory, self).__init__(*args, **kwargs)

    def buildProtocol(self, addr):
        return HeyResponderProtocol(self.process_info)


class HeyResponderProtocol(protocol.Protocol, object):
    def __init__(self, process_info, *args, **kwargs):
        self.process_info = process_info
        super(HeyResponderProtocol, self).__init__(*args, **kwargs)

    def dataReceived(self, data):
        if data == 'whatsup':
            self.whatsup()
        if data == 'stopit':
            self.stopit()

    def connectionLost(self, reason):
        if self.process_info.status in ['exited', 'ended', 'stopping']:
            reactor.stop()

    def stopit(self):
        self.transport.write('stopping server\n')
        self.process_info.status = 'stopping'

    def whatsup(self):
        output = ""
        while True:
            try:
                output += self.process_info.outQueue.get_nowait()
            except Empty:
                if output == "":
                    output = "nothing to report, sir\n"
                break

        self.transport.write(output)


class HeyProcessProtocol(protocol.ProcessProtocol, object):
    def __init__(self, process_info, *args, **kwargs):
        self.process_info = process_info
        super(HeyProcessProtocol, self).__init__(*args, **kwargs)

    def connectionMade(self):
        self.process_info.status = 'running'

    def outReceived(self, data):
        self.process_info.outQueue.put(data)

    def processExited(self, reason):
        self.process_info.status = 'exited'

    def processEnded(self, reason):
        self.process_info.status = 'ended'


class HeyServer(object):
    def __init__(self, command, port):
        process_info = ProcessInfo()
        self.proc = HeyProcessProtocol(process_info)
        reactor.spawnProcess(self.proc, command[0], command, usePTY=True)
        endpoint = TCP4ServerEndpoint(reactor, port)
        endpoint.listen(HeyResponderFactory(process_info))

    def run(self):
        reactor.run()


def start(command):
    host, port = "localhost", 9999

    server = HeyServer(command, port)
    server.run()
