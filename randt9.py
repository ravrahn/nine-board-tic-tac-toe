#!/usr/bin/python
import sys
import re
import socket
import random

PLAYER_X = "X"
PLAYER_O = "O"
PLAYER_NONE = "."

board = None


class Board:
    """A nine-board tic-tac-toe board"""
    player = ""
    current_board = 0
    last_move = (0, 0)
    boards = [[PLAYER_NONE for i in range(1, 10)] for j in range(1, 10)]

    def __init__(self, player):
        self.player = player

    def __str__(self):
        """Return a visual representation of the board"""
        string = "\n"
        boards = [self.boards[:3], self.boards[3:6], self.boards[6:9]]
        for j in range(0, 3):
            string += " "
            for i in range(0, len(boards[j])):
                string += " ".join(boards[j][i][:3])
                if i != len(boards[j])-1:
                    string += " | "
            string += "\n "
            for i in range(0, len(boards[j])):
                string += " ".join(boards[j][i][3:6])
                if i != len(boards[j])-1:
                    string += " | "
            string += "\n "
            for i in range(0, len(boards[j])):
                string += " ".join(boards[j][i][6:9])
                if i != len(boards[j])-1:
                    string += " | "
            if j != len(boards)-1:
                string += "\n ------+-------+------ "
            string += "\n"

        return string

    def add_move(self, move, current_board=None, is_me=True):
        """Add a move to the board."""
        if current_board is None:
            current_board = self.current_board

        if is_me:
            self.boards[current_board-1][move-1] = self.player
        elif self.player == PLAYER_X:
            self.boards[current_board-1][move-1] = PLAYER_O
        elif self.player == PLAYER_O:
            self.boards[current_board-1][move-1] = PLAYER_X

        self.last_move = (current_board, move)
        self.current_board = move

    def is_legal(self, move):
        """Given a move, check if it's legal"""
        return self.boards[self.current_board-1][move-1] == PLAYER_NONE


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def second_move(first_board, first_move):
    """Perform the second move and add the first to the board"""
    board.add_move(int(first_move), int(first_board), False)
    random_move()


def third_move(first_board, first_move, second_move):
    """Perform the third move and add the first two to the board"""
    board.add_move(int(first_move), int(first_board))
    board.add_move(int(second_move), board.current_board, False)
    random_move()


def next_move(last_move):
    """Perform a move and add the most recent one to the board"""
    board.add_move(int(last_move), board.current_board, False)
    random_move()


def random_move():
    """Attmept to make a move at random"""
    attempted_move = random.randint(1, 9)
    if board.is_legal(attempted_move):
        move(attempted_move)
    else:
        random_move()


def move(move):
    """Given an int between 0 and 8
       perform that move"""
    board.add_move(move)
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

command = "init.\n"

while "end" not in command and command != "":
    command = repr(s.recv(1024))
    # take action on the command(s) given

    # sometimes multiple commands are received at once
    # e.g. "start" and "second_move" or "third_move"
    # so we check for each individually, not with elifs
    # and extract the args with regex

    # start
    start_args = re.search(r"start\(([xo])\)", command)
    # initialise the board as the player we're assigned
    if start_args is not None:
        if start_args.group(1) == "x":
            board = Board(PLAYER_X)
        elif start_args.group(1) == "o":
            board = Board(PLAYER_O)

    # second_move
    second_move_args = re.search(r"second_move\(([1-9]),([1-9])\)", command)
    if second_move_args is not None:
        second_move(second_move_args.group(1), second_move_args.group(2))

    # third_move
    third_move_args = re.search(r"third_move\(([1-9]),([1-9]),([1-9])\)",
                                command)
    if third_move_args is not None:
        first_move = third_move_args.group(1)
        first_board = third_move_args.group(2)
        second_move = third_move_args.group(3)

        third_move(first_move, first_board, second_move)

    # next_move
    next_move_args = re.search(r"next_move\(([1-9])\)", command)
    if next_move_args is not None:
        next_move(next_move_args.group(1))

    # win or lose, it's just a game
    game_end_args = re.search(r"(win|lose|end)", command)
    if game_end_args is not None:
        print command, board
        break

    print command, board

s.close()
