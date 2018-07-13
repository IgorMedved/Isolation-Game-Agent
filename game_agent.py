"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
#import timeit



class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def get_linear_score (moves):
    """converts the number of moves a player has to a linear mobility score
    i.e if player has one move the score is 1, if player has two moves the score is 1+1/2, 3 moves 1+1/2+1/3, etc
        """
    count = 0
    for div in range(moves):
        count+=(1/(div+1))
    return count

def get_quad_score(moves):
    """converts the number of moves a player has to a quadratic mobility score
    i.e if player has one move the score is 1, if player has two moves the score is 1+1/4, 3 moves 1+1/4+1/9, etc
            """
    count = 0
    for div in range(moves):
        count+=(1/(div+1)/(div+1))
    return count

#@linear_score array stores all possible values of linear mobility values
#linear_score[1][3] - stores the value corresponding to 1 own move and 3
linear_score = [[-get_linear_score(x) + get_linear_score(y) for x in range(9)]for y in range(9)]
quad_score = [[-get_quad_score(x) + get_quad_score(y) for x in range(9)] for y in range(9)]
mixed_score = [[linear_score[i][j]*quad_score[i][j] if linear_score[i][j] > 0 else -linear_score[i][j]*quad_score[i][j] for j in range(9)]for i in range (9) ]



#mixed_score heuristic as described in report
def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return mixed_score[own_moves][opp_moves]

#quadratic score heuristic as described in report
def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # if own_moves == 0 and opp_moves != 0:
    #    return float("-inf")
    # elif opp_moves == 0 and own_moves != 0:
    #    return float("inf")

    return quad_score[own_moves][opp_moves]


#linear score heuristic as described in report
def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # if own_moves == 0 and opp_moves!=0:
    #    print (own_moves, opp_moves, 'lost')
    #    return float("-inf")
    # elif opp_moves==0 and own_moves!=0:
    #    print (own_moves, opp_moves, 'won')
    #    return float("inf")
    # print (linear_score[own_moves][opp_moves], own_moves, opp_moves)
    return linear_score[own_moves][opp_moves]


#improved score
def custom_score_4(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
        
        
    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - opp_moves)


#open score
def custom_score_5(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    #opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves)

#attmpt to estimate the number of moves available to a player until he runs out. Performs really badly in tests
def greedy_endgame_score(game,player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    gamecpy = game.copy()
    counter = 0
    #should_continue = True
    max_moves = game.get_max_moves()
    while True:
        counter+=1
        legal_moves = gamecpy.get_legal_moves()
        if not legal_moves:
            if gamecpy.active_player == player:
                return -counter+max_moves
            else:
                return counter - max_moves

        _, move = max([(open_move_score(gamecpy.forecast_move(m), gamecpy.active_player), m) for m in legal_moves])
        print (gamecpy.to_string(), move, 'player move computer', gamecpy.active_player == player)
        gamecpy.apply_move(move)


def open_move_score(game, player):
    """The basic evaluation function described in lecture that outputs a score
    equal to the number of moves open for your computer player on the board.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return float(len(game.get_legal_moves(player)))


# function used to modify improved score coefficient
def custom_score_6(game, player, alpha=1):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return own_moves-alpha*opp_moves



def custom_score61 (game,player):
    return custom_score_6(game,player, alpha=.1)
def custom_score62 (game,player):
    return custom_score_6(game,player, alpha=.2)
def custom_score63 (game,player):
    return custom_score_6(game,player, alpha=.3)
def custom_score64 (game,player):
    return custom_score_6(game,player, alpha=.4)
def custom_score65 (game,player):
    return custom_score_6(game,player, alpha=.5)
def custom_score66 (game,player):
    return custom_score_6(game,player, alpha=.6)
def custom_score67 (game,player):
    return custom_score_6(game,player, alpha=.7)
def custom_score68 (game,player):
    return custom_score_6(game,player, alpha=.8)
def custom_score69 (game,player):
    return custom_score_6(game,player, alpha=.9)
def custom_score611 (game,player):
    return custom_score_6(game,player, alpha=1.25)
def custom_score612 (game,player):
    return custom_score_6(game,player, alpha=1.5)
def custom_score613 (game,player):
    return custom_score_6(game,player, alpha=1.75)
def custom_score614 (game,player):
    return custom_score_6(game,player, alpha=2)

def custom_score615 (game,player):
    return custom_score_6(game,player, alpha=.01)
def custom_score616 (game,player):
    return custom_score_6(game,player, alpha=100)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    symmetry_count = 0
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=30.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.depth = 0
        self.TIMER_THRESHOLD = timeout
        self.best_map = {}
        self.opp_map = {}
        self.solved = False




class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """


    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            best_move = self.minimax(game, self.search_depth)

            return best_move

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        best_score = float('-inf')

        actions = game.get_legal_moves()
        if len(actions) > 0:
            best = actions[0]
        else:
            best = (-1,-1)
        if depth < 0:
            return -1, -1
        elif depth == 0:
            return best
        for action in actions:
            current_score = self.min_value (game.forecast_move(action), depth-1)
            if best_score < current_score:
                best = action
                best_score = current_score

        return best



    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if depth == 0 or game.is_loser(self) or game.is_winner(self):
            score = self.score(game, self)
            if score == float('-inf'):  # adjust the score, so that going deeper down the tree is better
                                        # than losing right away
                score = -10e18 / (self.search_depth-depth)
            elif score == float('inf'):  # also winning right away is better than postponing it by several moves
                score = 10e18 / (self.search_depth-depth)
            return score
        best_score = 10e18 / (self.search_depth-depth)
        actions = game.get_legal_moves()
        for action in actions:
            current_score = self.max_value(game.forecast_move(action), depth-1)
            if best_score > current_score:
                best_score = current_score
        return best_score

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth == 0 or game.is_loser(self) or game.is_winner(self):
            score = self.score(game, self)
            if score == float('-inf'):  # adjust the score, so that going deeper down the tree is better
                                        # than losing right away
                score = -10e18 / (self.search_depth-depth)
            elif score == float('inf'):  # also winning right away is better than postponing it by several moves
                score = 10e18 / (self.search_depth-depth)
            return score
        actions = game.get_legal_moves()

        best_score = -10e18 / (self.search_depth-depth)
        for action in actions:
            current_score = self.min_value(game.forecast_move(action), depth - 1)
            if best_score < current_score:
                best_score = current_score
        return best_score


# simple alphabetaPlayer without the optimization
class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. Use the same boards for min and max functions and revert it to the previous state
    instead of copying the whole thing
    """
    #counter = 0
    #WIN_SCORE = 1000

    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move = (-1, -1)
        for depth in range(1, len(game.get_blank_spaces())+1):
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                #self.depth = depth

                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration


        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


        actions = game.get_legal_moves()
        size = len(actions)
        if size == 0:
            return -1, -1

        best_score = float('-inf')
        for action in actions:
            current_score = self.min_value(game.forecast_move(action), depth-1, alpha, beta, depth)
            if best_score < current_score or best_score==float('-inf'):
                best = action
                best_score = current_score
            if best_score >= beta:
                return best
            if alpha < best_score:
                    alpha = best_score


        return best


    def min_value(self, game, depth, alpha, beta, max_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        actions = game.get_legal_moves()
        size = len(actions)
        #if self.depth == 0 or self.depth == depth: #This line might cause automated unit testing failure, but it is not an erroor
                                                    #  self.depth is the maximum depth of current iterative deepening phase
        #    print ('self.depth is  needed for better work of alpha beta algorithm. This is not an error and has been extensively tested, but it might fail automated testing',self.depth, depth)
        DEFAULT_SCORE = 10e18 / (max_depth-depth) # the deeper we proceed down the tree the smaller the absolute magnitude of
                                                    # Default score. This way we chose moves that pospone loss as far down the road
                                                    #as possible and choose the winning moves from shallower positions
        if size == 0:
            return DEFAULT_SCORE
        if depth == 0:
            return self.default_score(game, DEFAULT_SCORE)
        best_score = DEFAULT_SCORE

        for action in actions:
            current_score = self.max_value(game.forecast_move(action), depth-1, alpha, beta, max_depth)
            if best_score > current_score:
                best_score = current_score
            if best_score <= alpha:
                return best_score
            if beta > best_score:
                    beta = best_score

        return best_score

    def max_value(self, game, depth, alpha, beta, max_depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        #if self.depth == 0 or self.depth == depth: # This line might lead
                                                    # to automated error testing, but it is not an error!!! self.depth is the
                                                    # maximum depth of current iterative deepening phase
        #    print (self.depth, depth)

        actions = game.get_legal_moves()
        size = len(actions)
        DEFAULT_SCORE = - 10e18 / (max_depth - depth) # the deeper we proceed down the tree the smaller the absolute magnitude of
                                                    # Default score. This way we chose moves that pospone loss as far down the road
                                                    # as possible and choose the winning moves from shallower positions. This might lead
                                                    # to automated error testing, but it is not an error!!!
        if size == 0:
            return DEFAULT_SCORE
        if depth == 0:
            return self.default_score(game,DEFAULT_SCORE)

        best_score = DEFAULT_SCORE
        for action in actions:
            current_score = self.min_value(game.forecast_move(action), depth-1, alpha, beta, max_depth)
            if best_score < current_score:
                best_score = current_score
                if best_score >= beta:
                    return best_score
                if alpha < best_score:
                    alpha = best_score
        return best_score

    def default_score(self, game, DEFAULT_SCORE):
        score = self.score(game, self)
        if score == float('-inf'):  # adjust the score, so that going deeper down the tree is better
            #  than losing right away
            score = DEFAULT_SCORE
        elif score == float('inf'):  # also winning right away is better than postponing it by several moves
            score = -DEFAULT_SCORE
        return score

#the most optimized version of alphabetaplayer (it does not pass the interface test as it uses modifications in isolation.py)
#available optimizations:
#1) move ordering
#2) iterative deepening result caching
#3) apply_move reverse_move pattern instead of copying position with forecast_move speeding the program up and also saving memory
class AlphaBetaPlayer1(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. Use the same boards for min and max functions and revert it to the previous state
    instead of copying the whole thing
    """
    counter = 0
    WIN_SCORE = 1000 # if either player is able to score this means the position is won

    def get_move(self, game, time_left):
        self.time_left = time_left

        best_move = (-1, -1)
        for depth in range(1, self.search_depth +1):
            try:
                # The try/except block will automatically catch the exception
                # raised when the timer is about to expire.
                self.depth = depth

                best_move = self.alphabeta(game, depth)
                if self.solved:
                    break
            except SearchTimeout:
                #print(depth,'timeout')
                return best_move  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration


        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        if self.time_left() < self.TIMER_THRESHOLD:
            # print ('timed out in alp value', self.time_left())
            raise SearchTimeout()

        self.solved = False  # at the beginning of each move set this variable to false to find the best move
        actions = game.get_legal_moves()
        size = len(actions)
        if size == 0:
            self.solved = True
            return -1, -1

        location = game.hash()
        action_list = self.best_map.get(location)
        if action_list is None:
            self.best_map = {} # empty map
            plr2,plr1, init = game.check() # get positions for player 2, player 1 and initiative
            saved_depth = 0
            saved_score = float('-inf')
        else:
            saved_score, actions, saved_depth, (plr2, plr1, init) = action_list # used cache results if available
            if (plr2, plr1, init) != game.check(): # check that caching was correct
                print ("wrong position!!! at depth", 0)
                return (-1,-1)


        best_score = float('-inf')
        best_score_index = 0
        if saved_depth < depth:
            #gamecpy = game.copy() # we need to insure that the main board is not modified by apply_move reverse_move pattern
            #during timeout that's why copy here is needed if we were to use it, but it is quicker to use #apply move at this level
            for i in range(size):
                current_score = self.min_value(game.forecast_move(actions[i]), depth-1, alpha, beta)
                #gamecpy.reverse_move(saved_loc, actions[i]) # see previous comment
                saved_depth = depth
                if best_score < current_score:
                    best = actions[i]
                    best_score = current_score
                    best_score_index = i
                if best_score >= beta:
                    if best_score > self.WIN_SCORE or best_score < -self.WIN_SCORE:
                        self.solved = True # set solved to true to prevent further expansion with deeper level

                    #sort scores from
                    if best_score_index != 0:
                        actions[0], actions[best_score_index] = actions[best_score_index], actions[0]

                    self.best_map[location] = best_score, actions, saved_depth, (plr2, plr1, init)
                    return best
                if alpha < best_score:
                    alpha = best_score
        else:
            return actions[0]

        #print (best_score, best)
        #print (scores, depths, actions, 'after')

        if best_score > self.WIN_SCORE or best_score < -self.WIN_SCORE:
            #print ('solved', best_score, best)
            self.solved = True  # set solved to true to prevent further expansion with deeper level
        #sort scores in scores, depths, actions, save them in best_map[location]
        if best_score_index != 0:
            actions[0], actions[best_score_index] = actions[best_score_index], actions[0]
        self.best_map[location] = best_score, actions, saved_depth, (plr2, plr1, init)
        #print (self.best_map.get(location), 'after')
        return best


    def min_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print ('timed out in min value',self.time_left())
            raise SearchTimeout()

        actions = game.get_legal_moves()
        size = len(actions)
        DEFAULT_SCORE = 10e18 / (self.depth-depth)
        if size == 0:
            return DEFAULT_SCORE
        if depth == 0:
            return self.default_score(game, DEFAULT_SCORE)
        location = game.hash()
        action_list = self.opp_map.get(location)
        if action_list is None:
            if self.depth-depth ==1:
                self.opp_map = {} #empty opponent map if at 1st level in the search tree
            plr2, plr1, init = game.check()
            saved_depth = 0
            saved_score = DEFAULT_SCORE
        else:
            saved_score, actions, saved_depth, (plr2,plr1, init) = action_list
            if (plr2, plr1, init) != game.check():
                print ("wrong position!!! at depth", (self.depth-depth))
                return DEFAULT_SCORE
        best_score = DEFAULT_SCORE
        #print (depths, depth, depths[0]< depth)
        best_score_index = 0
        if saved_depth < depth:
            saved_loc = game.get_player_location(game.active_player)

            for i in range(len(actions)):
                #print (game.to_string(), 'apply move min value', actions[i], depth)
                current_score = self.max_value(game.apply_move(actions[i]), depth-1, alpha, beta)
                #print (game.to_string(), " before move_reversed min value", saved_loc)
                game.reverse_move(saved_loc, actions[i])
                #print (game.to_string(), " reversed min value")
                saved_depth = depth
                if best_score > current_score:
                    best_score = current_score
                    best_score_index = i
                if best_score <= alpha:
                    #sort scores from
                    if best_score_index!= 0:
                        actions[0], actions[best_score_index] = actions[best_score_index], actions[0]
                    self.opp_map[location] = best_score, actions, saved_depth, (plr2,plr1, init)
                    return best_score
                if beta > best_score:
                    beta = best_score
        else:
            return saved_score

        if best_score > self.WIN_SCORE or best_score < -self.WIN_SCORE:
            self.solved = True  # set solved to true to prevent further expansion with deeper level
        #sort scores in scores, depths, actions, save them in best_map[location]
        if best_score_index != 0:
            actions[0], actions[best_score_index] = actions[best_score_index], actions[0]
        self.opp_map[location] = best_score, actions, saved_depth, (plr2, plr1, init)
        return best_score

    def max_value(self, game, depth, alpha, beta):
        if self.time_left() < self.TIMER_THRESHOLD:
            # print ('timed out in max value', self.time_left())
            raise SearchTimeout()

        actions = game.get_legal_moves()
        size = len(actions)
        DEFAULT_SCORE = - 10e18 / (self.depth- depth)
        if size == 0:
            return DEFAULT_SCORE
        if depth == 0:
            return self.default_score(game,DEFAULT_SCORE)


        location = game.hash()
        action_list = self.best_map.get(location)
        if action_list is None:
            plr2,plr1,init = game.check()
            saved_depth = 0
            saved_score = DEFAULT_SCORE

        else:
            saved_score, actions, saved_depth, (plr2,plr1,init) = action_list
            if (plr2, plr1, init) != game.check():
                print ("wrong position!!! at depth", (self.depth-depth))
                return DEFAULT_SCORE
        best_score = DEFAULT_SCORE
        best_score_index = 0
        if saved_depth < depth:
            saved_loc = game.get_player_location(game.active_player)
            for i in range(len(actions)):
                #print (game.to_string(), 'apply move max value', actions[i], depth)
                current_score = self.min_value(game.apply_move(actions[i]), depth-1, alpha, beta)
                #print (game.to_string(), 'before reverse max value', saved_loc)
                game.reverse_move(saved_loc, actions[i])
                #print (game.to_string(), 'after reverse max value')
                saved_depth = depth
                if best_score < current_score:
                    best_score = current_score
                    best_score_index = i
                if best_score >= beta:
                    if best_score_index != 0:
                        actions[0], actions[best_score_index] = actions[best_score_index], actions[0]
                    self.best_map[location] = best_score, actions, saved_depth, (plr2,plr1,init)
                    return best_score
                if alpha < best_score:
                    alpha = best_score
        else:
            return saved_score
        if best_score_index != 0:
            actions[0], actions[best_score_index] = actions[best_score_index], actions[0]
        self.best_map[location] = best_score, actions, saved_depth, (plr2,plr1, init)
        return best_score

    def default_score(self, game, DEFAULT_SCORE):
        score = self.score(game, self)
        if score == float('-inf'):  # adjust the score, so that going deeper down the tree is better
            #  than losing right away
            score = DEFAULT_SCORE
        elif score == float('inf'):  # also winning right away is better than postponing it by several moves
            score = -DEFAULT_SCORE
        return score
