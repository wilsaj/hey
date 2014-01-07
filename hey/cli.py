"""hey

Usage:
  hey listen <command>
  hey whatsgoingon
  hey (-h | --help)
  hey --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from hey import client
from hey import server
from hey.version import __version__


def main():
    arguments = docopt(__doc__, version=__version__)

    if arguments.get('listen'):
        command = arguments.get('<command>').split()
        server.start(command)

    if arguments.get('whatsgoingon'):
        client.whatsup('ping')


if __name__ == '__main__':
    main()
