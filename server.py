# Server program
import socket, sys, threading, json, datetime
from pathlib import Path

loglock = threading.Lock()

def get_boards():
    path= Path('./board')
    boards = [x.name for x in path.iterdir() if x.is_dir()]
    if not boards:
        return ["ERROR", "no boards defined"]
    return boards


def get_messages(board_title):
    path = Path("./board/"+str(board_title))
    messages = []
    try:
        for x in path.iterdir():
            with x.open() as f:
                messages.append([x.name , f.read()])
    except FileNotFoundError:
        return ["ERROR", "Board does not exist"]
    messages.sort()
    del messages[100:]
    return messages


def post_message(message_details):

    datetimestr = str(datetime.datetime.now()).split(".")[0].replace("-", "").replace(" ","-").replace(":", "")
    path = Path("./board/" + message_details[0]+"/"+ datetimestr + "-" + message_details[1])
    path.touch()
    with open(path, "w") as f:
        f.write(message_details[2])


    return ["success"]

def process_data(data):
    data = json.loads(data)

    if len(data) >= 1:
        if data[0] == "GET_BOARDS":
            response = get_boards()
        elif len(data) == 2:
            if data[0] == "GET_MESSAGES":
                response = get_messages(data[1][0])
            elif data[0] == "POST_MESSAGE":
                response = post_message(data[1])
            else:
                response = ["ERROR", "invalid message"]
        else:
            response = ["ERROR", "invalid message"]
    else:
        response = ["ERROR","invalid message"]
    if response:

        if response[0] == "ERROR":
            status = "ERROR"
        else:
            status = "OK"
    else:
        status = "OK"
    return json.dumps(response).encode(), data[0], status




def handle_connection(conn, addr):
    data = b""
    while 1:

        segment = conn.recv(1024)
        if segment:
            data += segment
        else:
            break
    if data:
        data = data.decode()

        data, message_type, status = process_data(data)
        conn.sendall(data)
    conn.close()

    loglock.acquire()
    logpath = Path("./server.log")
    with open(str(logpath), "a") as logfile:
        logfile.write("\n"+str(datetime.datetime.now())+"    "+str(addr)+"    "+str(message_type)+"  "+status)
    loglock.release()


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
    thread = threading.Thread(target=handle_connection, args=(conn,addr))
    thread.start()

