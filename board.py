import copy

PLAYER_X = "X"
PLAYER_O = "O"
PLAYER_NONE = "."

MINIMAX_DEPTH = 4


class Board(object):
    """A nine-board tic-tac-toe board state"""
    player = ""
    current_board = 0
    last_move = 0
    last_board = 0
    boards = [[PLAYER_NONE for i in range(1, 10)] for j in range(1, 10)]
    x_score = 0
    o_score = 0
    children = []

    def __init__(self, player):
        self.player = player
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def add_children(self, children):
        self.children.extend(children)

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
        # print "x:", str(self.x_score)
        # print "o:", str(self.o_score)
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
                score += 1000000  # Like a billion
            elif num == 2:
                score += 10
            elif num == 1:
                score += 1
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

    def generate_tree(self, depth, is_me):
        """Generate a Tree from a given board"""
        new_board = copy.copy(self)

        if depth == 0:
            return new_board

        for next_board in new_board.next_boards(is_me):
            # for each board, generate all the next boards
            new_board.add_child(next_board.generate_tree(depth - 1, not is_me))

        return new_board
