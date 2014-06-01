#!/usr/bin/python
import sys
import re
import socket
import random
import board

current_board = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Tree(object):
    """A Tree with a list of Trees as children
        and a value (a Board)"""
    children = []
    value = None

    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)


def generate_tree(current_board, depth, is_me):
    """Generate a Tree from a given board"""
    states = Tree(current_board)

    if depth == 0:
        return states

    for next_board in current_board.next_boards(is_me):
        # for each board, generate all the next boards
        states.add_child(generate_tree(next_board, depth - 1, not is_me))

    return states


def random_move():
    """Make a move at random"""
    attempted_move = random.randint(1, 9)

    while not current_board.is_legal(attempted_move):
        attempted_move = random.randint(1, 9)

    move(attempted_move)


def minimax_move():
    """Make a move determined using a minimax algorithm"""
    move_tree = generate_tree(current_board, board.MINIMAX_DEPTH, False)

    best_board = None
    best_score = -1000000  # like a billion

    a = -1000000000
    b = 1000000000
    for child in move_tree.children:
        child_score = max_score(child, a, b, current_board.player)
        if child_score > best_score:
            best_board = child.value
            best_score = child_score

    print best_score

    attempted_move = best_board.last_move

    move(attempted_move)
    print attempted_move


def max_score(tree, a, b, original_player):
    """Perform a minimax with alpha-beta pruning 
        on a tree of Board objects to return the 
        score for the given board"""
    tree.value.player = original_player
    if len(tree.children) == 0:
        return tree.value.get_score()

    for child in tree.children:
        a = max(a, min_score(child, a, b, original_player))
        # child_score = random.randint(-100000, 100000)
        if b <= a:
            break
    return a


def min_score(tree, a, b, original_player):
    """Perform a minimax on a tree of Board objects
        to return the score for the given board"""
    tree.value.player = original_player
    if len(tree.children) == 0:
        return tree.value.get_score()

    for child in tree.children:
        b = min(b, max_score(child, a, b, original_player))
        # child_score = random.randint(-100000, 100000)
        if b <= a:
            break
    return b


#####################################
#                                   #
#            SERVER CODE            #
#                                   #
#####################################


def second_move(first_board, first_move):
    """Perform the second move and add the first to the current_board"""
    current_board.add_move(int(first_move), int(first_board), False)
    # random_move()
    minimax_move()


def third_move(first_board, first_move, second_move):
    """Perform the third move and add the first two to the current_board"""
    current_board.add_move(int(first_move), int(first_board))
    current_board.add_move(int(second_move), current_board.current_board, False)
    # random_move()
    minimax_move()


def next_move(last_move):
    """Perform a move and add the most recent one to the current_board"""
    current_board.add_move(int(last_move), current_board.current_board, False)
    # random_move()
    minimax_move()


def last_move(previous_move):
    """Add the last move to the current_board"""
    current_board.add_move(int(previous_move), current_board.current_board, False)


def move(move):
    """Given an int between 0 and 8,
        add it to the current_board, and send it to the server"""
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
