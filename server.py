# Server program
import socket
import sys
import threading

import json


def get_boards():
    return "get boards"


def get_messages(board_title):
    return "content of message board "+board_title[0]
def post_message(message_details):
    return "message posted"

def process_data(data):
    data = json.loads(data)

    if len(data) >= 1:
        if data[0] == "GET_BOARDS":
            response = get_boards()
        elif len(data) == 2:
            if data[0] == "GET_MESSAGES":
                response = get_messages(data[1])
            elif data[0] == "POST_MESSAGE":
                response = post_message(data[1])
            else:
                response = "ERROR"
        else:
            response = "ERROR"
    else:
        response = "ERROR"

    return json.dumps(response).encode()




def handle_connection(conn):
    data = b""
    while 1:

        segment = conn.recv(1024)
        if segment:
            data += segment
        else:
            break
    if data:
        data = process_data(data)
        conn.sendall(data)
    conn.close()



HOST = "127.0.0.1"
PORT = 12345


if len(sys.argv) > 1:
    HOST = sys.argv[1]
if len(sys.argv) > 2:
    PORT = sys.argv[2]

s = None

try:
    s = socket.socket()
except OSError as msg:
    s = None
try:
    s.bind((HOST,PORT))
    s.listen(1)
except OSError as msg:
    s.close()
    s = None
if s is None:
    print('could not open socket')
    sys.exit(1)

while 1:
    conn, addr = s.accept()
    thread = threading.Thread(target=handle_connection, args=(conn,))
    thread.start()

