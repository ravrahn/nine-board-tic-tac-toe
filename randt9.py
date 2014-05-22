#!/usr/bin/python
import sys
import socket
import random

s = socket.socket()
player = ""


def first_move():
    move = random.randint(1, 9)
    move = 5
    print player
    s.send(str(move))
    print "hello", player, "hello"


# make sure we have a port
if "-p" in sys.argv:
    portArg = sys.argv.index("-p") + 1
    port = int(sys.argv[portArg])
else:
    error = """Usage: %s -p <port>""" % sys.argv[0]
    sys.exit(error)

# connect to the server
host = socket.gethostname()
s.connect((host, port))

command = s.recv(1024)
print command

while "end" not in command:
    command = s.recv(1024)
    print command
    # if "start(x)." in command:
    #     player = "x"
    #     print player
    #     print "x"
    # elif "start(o)." in command:
    #     player = "o"
    #     print player
    #     print "o"
    # else:
    #     first_move()
    print command
