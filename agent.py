#!/usr/bin/python
import sys
import re
import socket
import random
import copy

PLAYER_X = "X"
PLAYER_O = "O"
PLAYER_NONE = "."

MINIMAX_DEPTH = 4

ONE_IN_A_ROW = 1
TWO_IN_A_ROW = 25
THREE_IN_A_ROW = 1000000

board = None

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

game_tree = None

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


class Board(object):
    """A nine-board tic-tac-toe board state"""
    player = ""
    current_board = 0
    last_move = 0
    last_board = 0
    boards = [[PLAYER_NONE for i in range(1, 10)] for j in range(1, 10)]
    x_score = 0
    o_score = 0

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

    def __copy__(self):
        board_copy = Board(copy.deepcopy(self.player))
        board_copy.boards = copy.deepcopy(self.boards)
        board_copy.last_move = copy.deepcopy(self.last_move)
        board_copy.x_score = copy.deepcopy(self.x_score)
        board_copy.o_score = copy.deepcopy(self.o_score)
        board_copy.current_board = copy.deepcopy(self.current_board)
        return board_copy

    def add_move(self, move, current_board=None, is_me=True):
        """Add a move to the board."""
        if current_board is None:
            current_board = self.current_board

        previous_x = self.__calculate_board_score(current_board, PLAYER_X)
        previous_o = self.__calculate_board_score(current_board, PLAYER_O)

        if is_me:
            self.boards[current_board-1][move-1] = self.player
        elif self.player == PLAYER_X:
            self.boards[current_board-1][move-1] = PLAYER_O
        elif self.player == PLAYER_O:
            self.boards[current_board-1][move-1] = PLAYER_X

        new_x = self.__calculate_board_score(current_board, PLAYER_X)
        new_o = self.__calculate_board_score(current_board, PLAYER_O)
        self.x_score = self.x_score - previous_x + new_x
        self.o_score = self.o_score - previous_o + new_o

        self.last_move = move
        self.last_board = current_board
        self.current_board = move

    def __calculate_board_score(self, current_board, player):
        score = 0
        winlines = []
        for a in range(0, 3):
            winlines.append(range(a*3, a*3+3))
            winlines.append(range(a, 9, 3))
        winlines.append(range(2, 8, 2))
        winlines.append(range(0, 9, 4))
        for winline in winlines:
            num = 0
            for i in winline:
                if self.boards[current_board-1][i] == player:
                    num += 1
                elif self.boards[current_board-1][i] != PLAYER_NONE:
                    num -= 3
            if num == 3:
                score += THREE_IN_A_ROW  # Like a billion
            elif num == 2:
                score += TWO_IN_A_ROW
            elif num == 1:
                score += ONE_IN_A_ROW
        return score

    def is_legal(self, move):
        """Given a move, check if it's legal"""
        return self.boards[self.current_board-1][move-1] == PLAYER_NONE

    def get_score(self):
        """Calculate the score of the board for the player"""
        if self.player == PLAYER_X:
            return self.x_score - self.o_score
        else:
            return self.o_score - self.x_score

    def next_boards(self, is_me):
        new_boards = []
        for i in range(1, 10):
            if (self.is_legal(i)):
                new_board = copy.copy(self)

                new_board.add_move(i, self.current_board, not is_me)

                new_boards.append(new_board)
        return new_boards


def generate_tree(current_board, depth, is_me):
    """Generate a Tree from a given board"""
    states = Tree(current_board)

    if depth == 0:
        return states

    for next_board in current_board.next_boards(is_me):
        # for each board, generate all the next boards
        states.add_child(generate_tree(next_board, depth - 1, not is_me))

    return states

def repopulate_tree(tree, depth, move):
    """Repopulates the lower layers of a given tree"""
    for child in tree.children:
        if child.last_move == move:
            tree = child
            break
    tree = repopulate_tree_recurse(tree, depth, True)
    return tree

def repopulate_tree_recurse(tree, depth, is_me):
    if depth == 0:
        return tree
    elif len(tree.children) > 0:
        for child in tree.children:
            repopulate_tree_recurse(child, depth-1, not is_me)
    else:
        board = tree.value
        for next_board in board.next_boards(is_me):
            tree.add_child(generate_tree(next_board, depth - 1, not is_me))
    return tree


def random_move():
    """Make a move at random"""
    attempted_move = random.randint(1, 9)

    while not board.is_legal(attempted_move):
        attempted_move = random.randint(1, 9)

    move(attempted_move)

def alphabeta_move():
    move_tree = generate_tree(board, MINIMAX_DEPTH, False)
    a = -10000000
    b =  10000000
    best_board = game_tree
    for child in game_tree.children:
        olda = a
        a = max(a, alphabeta_recurse(child, MINIMAX_DEPTH-1, a, b, False))
        if a > olda:
            best_board = child
    attempted_move = best_board.value.last_move
    game_tree = best_board
    move(attempted_move)
    print attempted_move


def alphabeta_recurse(node, depth, a, b, maximizing_player):
    best = node
    if depth == 0:
        return node.value.get_score()
    if maximizing_player == True:
        for child in node.children:
            a = max(a, alphabeta_recurse(child, depth - 1, a, b, False))
            if b <= a:
                break
        return a
    if maximizing_player == False:
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


def second_move(first_board, first_move):
    """Perform the second move and add the first to the board"""
    board.add_move(int(first_move), int(first_board), False)
    game_tree = generate_tree(board, MINIMAX_DEPTH, False)
    alphabeta_move()


def third_move(first_board, first_move, second_move):
    """Perform the third move and add the first two to the board"""
    board.add_move(int(first_move), int(first_board))
    board.add_move(int(second_move), board.current_board, False)
    game_tree = generate_tree(board, MINIMAX_DEPTH, False)
    alphabeta_move()


def next_move(last_move):
    """Perform a move and add the most recent one to the board"""
    board.add_move(int(last_move), board.current_board, False)
    game_tree = repopulate_tree(game_tree, MINIMAX_DEPTH, last_move)
    alphabeta_move()


def last_move(previous_move):
    """Add the last move to the board"""
    board.add_move(int(previous_move), board.current_board, False)


def move(move):
    """Given an int between 0 and 8,
        add it to the board, and send it to the server"""
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

    # last_move
    last_move_args = re.search(r"last_move\(([1-9])\)", command)
    if last_move_args is not None:
        last_move(last_move_args.group(1))

    print command, board

    # win or lose, it's just a game
    game_end_args = re.search(r"(win|lose|end)", command)
    if game_end_args is not None:
        break

print "We're done here."
s.close()
