import socket


def stopit():
    _send_message('stopit')


def whatsup():
    _send_message('whatsup')


def _send_message(message):
    HOST, PORT = "localhost", 9999

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(message)

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()

    print "Sent:     {}".format(message)
    print "Received: {}".format(received)

    return received
