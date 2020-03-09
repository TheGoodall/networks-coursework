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





# Function to make a connection to the server, and send the request passed into it, returning the result
def make_request(request):

    # Creating the socket
    try:
        s=socket.socket()
    except OSError:
        print("could not open socket")
        sys.exit(1)
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
    data = data.decode()
    s.close()

    return json.loads(data)





boards = make_request(["GET_BOARDS"])

if boards:
    if boards[0] == "ERROR":
        print(boards[0] + " - " + boards[1])


def check_board_num(num):
    try:
        num = int(num)
    except ValueError:
        return False
    if num > 0 and num <= len(boards):
        return num
    else:
        return False


output = "Message boards: \n"

for i, board in enumerate(boards):
    output += str(i+1) +" - "+  board + "\n"

output += "\nChoose one of the following:\n<a number> - View the board corresponding to that number\nPOST - post to a board\nQUIT - quit the program"
print(output)

while 1:
    choice = str(input("> "))

    num = check_board_num(choice)
    if choice == "QUIT":
        sys.exit(0)
    elif choice == "POST":
        choice = input("Choose a board to post to:\n> ")
        num = check_board_num(choice)
        if num:
            title = input("Write a title:\n> ")
            message = input("Write a message:\n> ")
            response = make_request(["POST_MESSAGE",[boards[num-1], title, message]])
            if response:
                if response[0] == "ERROR":
                    print(response[0] + " - " + response[1])
        else:
            print("ERROR, not a board")
            continue

    elif num:
        response = make_request(["GET_MESSAGES", [boards[num-1]]])
        if response:
            if response[0] == "ERROR":
                print(response[0] + " - " + response[1])
        for message in response:
            print(message)
            title = message[0].replace("_", " ")
            body = message[1]
            date = title.split("-")[0:2]
            time = date[1]
            date = date[0]
            date = date[6:8]+"/"+date[4:6]+"/"+date[0:4]
            time = time[0:2]+":"+time[2:4]+":"+time[4:6]
            title = title.split("-")[-1]
            print("title: "+str(title)+"\ndate: "+str(date)+" - "+str(time)+"\nmessage: "+str(body)+"\n\n")
    else:
        print("ERROR, not a valid command")
        continue



