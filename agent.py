#!/usr/bin/python
import sys
import re
import socket
import random
import board

#####################################
#                                   #
#           DECISION CODE           #
#                                   #
#####################################

current_board = None

# MINIMAX_DEPTH = 5

ONE_IN_A_ROW = 1
TWO_IN_A_ROW = 25
THREE_IN_A_ROW = 1000000


def random_move():
    """Make a move at random"""
    global current_board

    attempted_move = random.randint(1, 9)

    while not current_board.is_legal(attempted_move):
        attempted_move = random.randint(1, 9)

    move(attempted_move)


def alphabeta_move():
    move_tree = current_board.generate_tree(board.MINIMAX_DEPTH, False)
    a = -10000000
    b =  10000000
    best_board = move_tree
    for child in move_tree.children:
        olda = a
        a = max(a, alphabeta_recurse(child, board.MINIMAX_DEPTH-1, a, b, False))
        if a > olda:
            best_board = child
    attempted_move = best_board.last_move

    move(attempted_move)
    print attempted_move


def alphabeta_recurse(node, depth, a, b, maximizing_player):
    best = node
    if depth == 0:
        return node.get_score()
    if maximizing_player:
        for child in node.children:
            a = max(a, alphabeta_recurse(child, depth - 1, a, b, False))
            if b <= a:
                break
        return a
    if not maximizing_player:
        for child in node.children:
            b = min(b, alphabeta_recurse(child, depth - 1, a, b, True))
            if b <= a:
                break
        return b


#####################################
#                                   #
#            SERVER CODE            #
#                                   #
#####################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def second_move(first_board, first_move):
    """Perform the second move and add the first to the current_board"""
    global current_board
    current_board.add_move(int(first_move), int(first_board), False)
    # random_move()
    alphabeta_move()


def third_move(first_board, first_move, second_move):
    """Perform the third move and add the first two to the current_board"""
    global current_board
    current_board.add_move(int(first_move), int(first_board))
    current_board.add_move(int(second_move), current_board.current_board, False)
    # random_move()
    alphabeta_move()


def next_move(last_move):
    """Perform a move and add the most recent one to the current_board"""
    global current_board
    current_board.add_move(int(last_move), current_board.current_board, False)
    # random_move()
    alphabeta_move()


def last_move(previous_move):
    """Add the last move to the current_board"""
    global current_board
    current_board.add_move(int(previous_move), current_board.current_board, False)


def move(move):
    """Given an int between 0 and 8,
    add it to the current_board, and send it to the server"""
    global current_board
    current_board.add_move(move)
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
            current_board = board.Board(board.PLAYER_X)
        elif start_args.group(1) == "o":
            current_board = board.Board(board.PLAYER_O)

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

    # last_move
    last_move_args = re.search(r"last_move\(([1-9])\)", command)
    if last_move_args is not None:
        last_move(last_move_args.group(1))

    print command, current_board

    # win or lose, it's just a game
    game_end_args = re.search(r"(win|lose|draw|end)", command)
    if game_end_args is not None:
        break

print "We're done here."
s.close()
