#!/usr/bin/python
import sys
import socket
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
player = ""


def second_move(command):
    move()


def third_move(command):
    move()


def next_move(command):
    move()


def move():
    move = random.randint(1, 9)
    print move
    s.sendall(str(move) + "\n")


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

command = "init."

while "end" not in command and command != "":
    command = repr(s.recv(1024))
    print command
    if "start(x)." in command:
        player = "x"
    elif "start(o)." in command:
        player = "o"
    if "second_move" in command:
        second_move(command)
    elif "third_move" in command:
        third_move(command)
    elif "next_move" in command:
        next_move(command)

s.close()
