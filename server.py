# Echo server program
import socket
import sys
import threading


def process_data(data):

    return "1"



def handle_connection(conn):
    with conn:
        data = conn.recv(1024)
        if data:
            data = process_data(data)
            conn.send(data)

HOST = "127.0.0.1"
PORT = 12345
s = None

for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
while 1:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_connection, args=(conn,))
    thread.start()
