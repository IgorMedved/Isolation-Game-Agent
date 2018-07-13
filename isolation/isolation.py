"""
This file contains the `Board` class, which implements the rules for the
game Isolation as described in lecture, modified so that the players move
like knights in chess rather than queens.

You MAY use and modify this class, however ALL function signatures must
remain compatible with the defaults provided, and none of your changes will
be available to project reviewers.
"""
import random
import timeit
from copy import copy

TIME_LIMIT_MILLIS = 700


class Board(object):
    """Implement a model for the game Isolation assuming each player moves like
    a knight in chess.

    Parameters
    ----------
    player_1 : object
        An object with a get_move() function. This is the only function
        directly called by the Board class for each player.

    player_2 : object
        An object with a get_move() function. This is the only function
        directly called by the Board class for each player.

    width : int (optional)
        The number of columns that the board should have.

    height : int (optional)
        The number of rows that the board should have.
    """
    BLANK = 0
    NOT_MOVED = None
    directions = ([(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)])

    def __init__(self, player_1, player_2, width=7, height=7):
        self.width = width
        self.height = height
        self.move_count = 0
        self._player_1 = player_1
        self._player_2 = player_2
        self._active_player = player_1
        self._inactive_player = player_2

        # The last 3 entries of the board state includes initiative (0 for
        # player 1, 1 for player 2) player 2 last move, and player 1 last move
        self._board_state = [Board.BLANK] * (width * height + 3)
        self._board_state[-1] = Board.NOT_MOVED
        self._board_state[-2] = Board.NOT_MOVED
        
        #initialize available move map:
        #if not move_map:
         #   initializeMoveMap()
        #else
        #    self.move_map = move_map

    def hash(self):
        return str(self._board_state).__hash__()

    @property
    def active_player(self):
        """The object registered as the player holding initiative in the
        current game state.
        """
        return self._active_player

    def check(self):
        return self._board_state[-1], self._board_state[-2], self._board_state[-3]

    @property
    def inactive_player(self):
        """The object registered as the player in waiting for the current
        game state.
        """
        return self._inactive_player

    def get_opponent(self, player):
        """Return the opponent of the supplied player.

        Parameters
        ----------
        player : object
            An object registered as a player in the current game. Raises an
            error if the supplied object is not registered as a player in
            this game.

        Returns
        -------
        object
            The opponent of the input player object.
        """
        if player == self._active_player:
            return self._inactive_player
        elif player == self._inactive_player:
            return self._active_player
        raise RuntimeError("`player` must be an object registered as a player in the current game.")

    def copy(self):
        """ Return a deep copy of the current board. """
        new_board = Board(self._player_1, self._player_2, width=self.width, height=self.height)
        new_board.move_count = self.move_count
        new_board._active_player = self._active_player
        new_board._inactive_player = self._inactive_player
        new_board._board_state = copy(self._board_state)
        return new_board

    def forecast_move(self, move):
        """Return a deep copy of the current game with an input move applied to
        advance the game one ply.

        Parameters
        ----------
        move : (int, int)
            A coordinate pair (row, column) indicating the next position for
            the active player on the board.

        Returns
        -------
        isolation.Board
            A deep copy of the board with the input move applied.
        """
        new_board = self.copy()
        new_board.apply_move(move)
        return new_board

        
    def move_is_legal(self, move):
        """Test whether a move is legal in the current game state.

        Parameters
        ----------
        move : (int, int)
            A coordinate pair (row, column) indicating the next position for
            the active player on the board.

        Returns
        -------
        bool
            Returns True if the move is legal, False otherwise
        """
        idx = move[0] + move[1] * self.height
        return (0 <= move[0] < self.height and 0 <= move[1] < self.width and
                self._board_state[idx] == Board.BLANK)

    def get_blank_spaces(self):
        """Return a list of the locations that are still available on the board.
        """
        return [(i, j) for j in range(self.width) for i in range(self.height)
                if self._board_state[i + j * self.height] == Board.BLANK]

    def get_max_moves(self):
        return self.height*self.width-self.move_count

    def issymmetrical(self):
        """
        Determining whether there is a symmetry in the position is extremely important, because it is easy to show that
        if one of the players was able to take the position symmetrical to it's opponent, the game can be won following
        a very simple strategy. For example on any board of size nxm where both n and m are even player 2 will always
        win by responding with a move that reflects the position of player 1. Say the board size is 4 by 4. Then in
        response to any move by player 1, player 2 can take the position that reflects player1 move with respect to the
        center. In response to move b2 by player 1 player 2 goes to c3. In this position player 1 has 4 moves:
        a4, c4, d3, d1.
        Player 2 job is to maintain the symmetry. Response to a4 : d1, to c4 : b1, to d3: a2, to d1 : a4. Each responce
        maintains the symmetry around the center. It is guaranteed that player 1 would run out of moves first.
        The center symmetry strategy works for player 2 on any boards if both dimensions are even, or one dimension is
        even and another is odd. Furthermore it works as a special case for the board of sizes 3x3, nx1 and 1xn.
        If the size of the board is nxm where both n and m are odd, there exist one square in the center of the board that
        the player 2 can't reflect. However if the center square was previously occupied and the position is symmetrical
        then player 1 can use the strategy to win the game.
        There are 3 more symmetry strategies that exist:
        1) symmetry about horizontal center line
        2) symmetry about vertical center line
        3) If the board is of size nxn symmetry around diagonals

        symmetry about horizontal center line:
        It works similar to symmetry around center. When the width of the board is even then the center line divides
        the board along the line that goes between the two center fields. Given the same example of 4 by 4 board and
        player 1 moving to b2 the new correspondense square for player 2 is c2 instead of c3,
        the response to a4: d4, to c4: b:4, to d3:a3, to d1:a1, and again player2 wins in the end by maintaining
        symmetry each turn.
        When the board width is an odd number the center line goes through the center column. To create conditions for
        maintaining symmetry all the squares on the center line must be umavailable. Player 1 wins if he can achieve
        symmetry after all the squares on the center line are filled or unreachable

        Symmetry about vertical line:
        See notes about symmetry about horizontal line

        Symmetry about the diagonal.
        The symmetry about the diagonal works in manner similar to symmetry around center lines, but occurs only
        when the board is square. The symmetry can only be achieved if all the squares on the diagonal in question are
        unreachable. If the board height is odd the symmetry benefits player1, if the height is even player 2 benefits

        Furthermore. player 1 can only benefit from symmetry if both n and m are odd, but neither is 1, and the board is
        not 3 by 3,
        Player 1 can never benefit from symmetry if either n or m or both are even
        Player 2 can benefit from symmetry in positions where n and m are both odd (except 3x3 and nx1 and 1xm

        Note!!!!
        This function does not guarantee to find symmetry in all cases
        It sacrifices accuracy for speed. For example when checking for symmetry around the center on boards where
        both height and widht are odd the symmetrical position can exist in cases where center square is unavailable
        rather than filled.
        Similarly the center lines and diagonals have to only be unavailable not filled

        along major dia
        :return:
        True if the position has any symmetry
        False otherwise. Note that for special boards of 1xm and nx1 the symmetry is also false by default!!!
        """

        if self.width == 1 or self.height==1:
            return False

        h_opp, w_opp = self.get_player_location(self._inactive_player)
        h_active, w_active = self.get_player_location(self.active_player)

        if self.width == 3 and self.height == 3:
            if self._active_player == self._player_1:
                if self.check_center_sym(h_opp, w_opp, h_active, w_active):
                    return True
            return False

        elif self.width % 2 == 1 and self.height % 2 == 1:
            if self.active_player == self._player_2:
                mid_i = self.width//2
                mid_j = self.height//2
                # check that middle square is filled
                if self._board_state[mid_i + mid_j * self.height] == Board.BLANK:
                    off_center = self.__get_moves((mid_i, mid_j))
                    if len(off_center) == 0:
                        pass
                    else:
                        return False #strictly speaking the middle position needs to be unavailable rather than filled to guarantee no symmetry
                            #however the check for symmetry needs to be fast and accuracy is sacrificed for speed
                if self.check_center_sym(h_opp, w_opp,  h_active, w_active):
                    return True
                if self.check_horizontal_sym(h_opp, w_opp,  h_active, w_active):
                    return True
                if self.check_vertical_sym(h_opp, w_opp,  h_active, w_active):
                    return True
                if self.width == self.height:
                    if self.check_diag1_sym(h_opp, w_opp,  h_active, w_active):
                        return True
                    if self.check_diag2_sym(h_opp, w_opp,  h_active, w_active):
                        return True
            return False
        elif self._active_player == self._player_1:
            if self.check_center_sym(h_opp, w_opp,  h_active, w_active):
                return True
            if self.check_horizontal_sym(h_opp, w_opp,  h_active, w_active):
                return True
            if self.check_vertical_sym(h_opp, w_opp, h_active, w_active):
                return True
            if self.width == self.height:
                if self.check_diag1_sym(h_opp, w_opp, h_active, w_active):
                    return True
                if self.check_diag2_sym(h_opp, w_opp, h_active, w_active):
                    return True

        return False

    def check_center_sym(self, h_opp, w_opp,  h_active, w_active):
        """Assumes that the center square was already checked

        returns True if symmetry around the center exists False otherwise"""

        # position symmetrical to h, w is self.height - h - 1, self.width -w - 1 or to idx  :  boardArea-idx

        # player locations are symmetrical
        if (h_active, w_active) == (self.height - h_opp -1, self.width - w_opp -1):
            # all squares are filled symmetrically
            for idx in range((self.width*self.height)//2-1):
                if self._board_state[idx] != self._board_state[self.width*self.height-1-idx]:
                    return False
            #print ('Found center sym')
            return True
        return False

    def check_horizontal_sym(self, h_opp, w_opp,  h_active, w_active):
        """

        :return: True if there is symmetry around horizontal center line False otherwise
        """

        #position symmetrical to h,w is self.height-h-1 , w or to idx
        # player locations are symmetrical
        if (h_active,w_active) == (self.height - h_opp -1, w_opp):
            # check center line is filled
            if self.height%2 ==1:
                for idx in range(self.height//2,self.height*self.width, self.height):
                    if self._board_state[idx] == self.BLANK: # not an exact condition for absense of symmetry
                        return False

            for w in range(self.width):
                for h in range(self.height//2):
                    idx = h + w*self.height
                    if self._board_state[idx] != self._board_state[idx-2*h+self.height-1]:
                        return False
            #print ('Found horizontal sym')
            return True
        return False

    def check_vertical_sym(self, h_opp, w_opp,  h_active, w_active):
        """

        :return: True if there is symmetry around vertical center line False otherwise
        """
        # position symmetrical to h,w is h , self.width- w -1 or to idx
        # player locations are symmetrical
        if (h_active, w_active) == (h_opp, self.width - w_opp -1):
            size = self.width*self.height
            middle_l = self.height*(self.width//2)
            middle_r = self.height* (self.height//2 +1)
            # check center line is filled
            if self.width%2 == 1:
                for idx in range (middle_l, middle_r):
                    if self._board_state[idx] == self.BLANK:   # not an exact condition for absence of symmetry
                        return False
            for idx in range (middle_l):
                if self._board_state[idx] != self._board_state[size+idx - self.height*(2*(idx//self.height)+1)]:
                    return False
            #print ('Found vertical sym')
            return True
        return False

    def check_diag1_sym(self, h_opp, w_opp,  h_active, w_active):
        """
        :return: True if there is symmetry around diagonal going from 0,0 corner to n-1, n-1 corner

        """

        # position symmetrical to h,w is w,h
        # player locations are symmetrical
        if (h_active, w_active) == (w_opp, h_opp):
            # check diagonal filled
            for idx in range (0, self.height*self.width, self.height+1):
                if self._board_state[idx] == self.BLANK and idx != self.height*self.width//2 :    #not an exact condition for absence of symmetry
                    return False

            idx = -1
            for w in range (self.width-1):
                idx += (w+1)
                sym = idx
                for h in range (w+1, self.height):
                    idx +=1
                    sym += self.height
                    if self._board_state[idx]!= self._board_state[sym]:
                        return False
            print ('Found diag1 sym')
            return True
        return False

    def check_diag2_sym(self, h_opp, w_opp, h_active, w_active):
        """
        :return: True if there is symmetry around diagonal going from (n-1,0 to 0,n-1) False otherwise

        """

        # position symmetrical to h,w is self.width-w_opp-1, self.height- h_opp-1
        # player locations are symmetrical
        if (h_active, w_active) == (self.width-w_opp-1, self.height- h_opp-1):
            # check diagonal filled
            for idx in range(self.height-1, self.height * self.width, self.height -1):
                if self._board_state[idx] == self.BLANK and idx != self.height*self.width//2:  # not an exact condition for absence of symmetry
                    return False

            idx = -self.height
            for w in range(self.width - 1):
                idx += (self.height+self.height-w-1)
                sym = idx
                for h in range(self.height - w -1):
                    idx -= 1
                    sym += self.height
                    if self._board_state[idx] != self._board_state[sym]:
                        return False
            print ('Found diag2 sym')
            return True
        return False


    def get_player_location(self, player):
        """Find the current location of the specified player on the board.

        Parameters
        ----------
        player : object
            An object registered as a player in the current game.

        Returns
        -------
        (int, int) or None
            The coordinate pair (row, column) of the input player, or None
            if the player has not moved.
        """
        if player == self._player_1:
            if self._board_state[-1] == Board.NOT_MOVED:
                return Board.NOT_MOVED
            idx = self._board_state[-1]
        elif player == self._player_2:
            if self._board_state[-2] == Board.NOT_MOVED:
                return Board.NOT_MOVED
            idx = self._board_state[-2]
        else:
            raise RuntimeError(
                "Invalid player in get_player_location: {}".format(player))
        w = idx // self.height
        h = idx % self.height
        return (h, w)

    def get_legal_moves(self, player=None):
        """Return the list of all legal moves for the specified player.

        Parameters
        ----------
        player : object (optional)
            An object registered as a player in the current game. If None,
            return the legal moves for the active player on the board.

        Returns
        -------
        list<(int, int)>
            The list of coordinate pairs (row, column) of all legal moves
            for the player constrained by the current game state.
        """
        if player is None:
            player = self.active_player
        return self.__get_moves(self.get_player_location(player))

    def apply_move(self, move):
        """Move the active player to a specified location.

        Parameters
        ----------
        move : (int, int)
            A coordinate pair (row, column) indicating the next position for
            the active player on the board.
        """
        idx = move[0] + move[1] * self.height
        last_move_idx = int(self.active_player == self._player_2) + 1
        self._board_state[-last_move_idx] = idx
        self._board_state[idx] = 1
        self._board_state[-3] ^= 1
        self._active_player, self._inactive_player = self._inactive_player, self._active_player
        self.move_count += 1

        return self

    def reverse_move(self, previous_loc, current_loc):
        """Take a step back
        param previous_loc location where the player was
        param rev location where the player is now"""
        idx = previous_loc[0] + previous_loc[1]*self.height
        revidx = current_loc[0] +  current_loc[1]*self.height
        prev_move_idx = int(self.active_player == self._player_1) +1
        self._board_state[revidx] = self.BLANK
        self._board_state[-prev_move_idx] = idx

        self._board_state[-3] ^= 1

        self._active_player, self._inactive_player = self._inactive_player, self._active_player
        self.move_count -= 1

    def is_winner(self, player):
        """ Test whether the specified player has won the game. """
        return player == self._inactive_player and not self.get_legal_moves(self._active_player)

    def is_loser(self, player):
        """ Test whether the specified player has lost the game. """
        return player == self._active_player and not self.get_legal_moves(self._active_player)

    def utility(self, player):
        """Returns the utility of the current game state from the perspective
        of the specified player.

                    /  +infinity,   "player" wins
        utility =  |   -infinity,   "player" loses
                    \          0,    otherwise

        Parameters
        ----------
        player : object (optional)
            An object registered as a player in the current game. If None,
            return the utility for the active player on the board.

        Returns
        ----------
        float
            The utility value of the current game state for the specified
            player. The game has a utility of +inf if the player has won,
            a value of -inf if the player has lost, and a value of 0
            otherwise.
        """
        if not self.get_legal_moves(self._active_player):

            if player == self._inactive_player:
                return float("inf")

            if player == self._active_player:
                return float("-inf")

        return 0.

    def __get_moves(self, loc):
        """Generate the list of possible moves for an L-shaped motion (like a
        knight in chess).
        """
        if loc == Board.NOT_MOVED:
            return self.get_blank_spaces()

        r, c = loc

        valid_moves = [(r + dr, c + dc) for dr, dc in self.directions
                       if self.move_is_legal((r + dr, c + dc))]
        random.shuffle(valid_moves)
        return valid_moves

    def print_board(self):
        """DEPRECATED - use Board.to_string()"""
        return self.to_string()

    def to_string(self, symbols=['1', '2']):
        """Generate a string representation of the current game state, marking
        the location of each player and indicating which cells have been
        blocked, and which remain open.
        """
        p1_loc = self._board_state[-1]
        p2_loc = self._board_state[-2]

        col_margin = len(str(self.height - 1)) + 1
        prefix = "{:<" + "{}".format(col_margin) + "}"
        offset = " " * (col_margin + 3)
        out = offset + '   '.join(map(str, range(self.width))) + '\n\r'
        for i in range(self.height):
            out += prefix.format(i) + ' | '
            for j in range(self.width):
                idx = i + j * self.height
                if not self._board_state[idx]:
                    out += ' '
                elif p1_loc == idx:
                    out += symbols[0]
                elif p2_loc == idx:
                    out += symbols[1]
                else:
                    out += '-'
                out += ' | '
            out += '\n\r'

        return out

    def play(self, time_limit=TIME_LIMIT_MILLIS):
        """Execute a match between the players by alternately soliciting them
        to select a move and applying it in the game.

        Parameters
        ----------
        time_limit : numeric (optional)
            The maximum number of milliseconds to allow before timeout
            during each turn.

        Returns
        ----------
        (player, list<[(int, int),]>, str)
            Return multiple including the winning player, the complete game
            move history, and a string indicating the reason for losing
            (e.g., timeout or invalid move).
        """
        move_history = []

        time_millis = lambda: 1000 * timeit.default_timer()

        while True:

            legal_player_moves = self.get_legal_moves()
            game_copy = self.copy()

            move_start = time_millis()
            time_left = lambda : time_limit - (time_millis() - move_start)
            curr_move = self._active_player.get_move(game_copy, time_left)
            move_end = time_left()

            if curr_move is None:
                curr_move = Board.NOT_MOVED

            if move_end < 0:
                return self._inactive_player, move_history, "timeout"

            if curr_move not in legal_player_moves:
                if len(legal_player_moves) > 0:
                    return self._inactive_player, move_history, "forfeit"
                return self._inactive_player, move_history, "illegal move"

            move_history.append(list(curr_move))

            self.apply_move(curr_move)

    def play_extra(self, time_limit=TIME_LIMIT_MILLIS):
        """Execute a match between the players by alternately soliciting them
        to select a move and applying it in the game.

        Parameters
        ----------
        time_limit : numeric (optional)
            The maximum number of milliseconds to allow before timeout
            during each turn.

        Returns
        ----------
        (player, list<[(int, int),]>, str)
            Return multiple including the winning player, the complete game
            move history, and a string indicating the reason for losing
            (e.g., timeout or invalid move).
        """
        move_history = []

        time_millis = lambda: 1000 * timeit.default_timer()

        while True:

            legal_player_moves = self.get_legal_moves()
            game_copy = self.copy()

            move_start = time_millis()
            time_left = lambda : time_limit - (time_millis() - move_start)
            curr_move = self._active_player.get_move(game_copy, time_left)
            move_end = time_left()

            if curr_move is None:
                curr_move = Board.NOT_MOVED

            if move_end < 0:
                return self._inactive_player, move_history, "timeout"

            if curr_move not in legal_player_moves:
                if len(legal_player_moves) > 0:
                    return self._inactive_player, move_history, "forfeit"
                return self._inactive_player, move_history, "illegal move"

            move_history.append(list(curr_move))

            self.apply_move(curr_move)
