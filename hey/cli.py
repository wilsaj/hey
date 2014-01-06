"""hey

Usage:
  hey listen
  hey whatsgoingon
  hey (-h | --help)
  hey --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt

from hey.version import __version__


def main():
    arguments = docopt(__doc__, version=__version__)
    print arguments


if __name__ == '__main__':
    main()
