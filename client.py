# client program
import socket
import sys

import json

HOST = '127.0.0.1'
PORT = 12345

# Using arguments (if they exist) to set the host and port
if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PORT = sys.argv[2]

# Creating the socket
try:
    s=socket.socket()
except OSError:
    print("could not open socket")
    sys.exit(1)




# Function to make a connection to the server, and send the request passed into it, returning the result
def make_request(request):

    try:
        s.connect((HOST,PORT))
    except OSError as msg:
        s.close()


    if s is None:
        print('could not open socket')
        sys.exit(1)

    s.sendall(json.dumps(request).encode())
    s.shutdown(socket.SHUT_WR)
    data = b""
    while 1:
        segment = s.recv(1024)
        if segment:
            data += segment
        else:
            break
    s.close()
    return data





data = make_request(["GET_BOARDS"])

print(data)
