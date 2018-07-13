#this function converts the number of moves into move score
# i.e moves = 0 => score = 0; moves = 1 score = 1, moves = 2 => score = 1+1/2 = 1.5, moves = 3 => score = 1 +1/2+1/3,etc
def get_linear_score (moves):
    """converts the number of moves a player has to a linear mobility score
    i.e if player has one move the score is 1, if player has two moves the score is 1+1/2, 3 moves 1+1/2+1/3, etc
        """
    count = 0
    for div in range(moves):
        count+=(1/(div+1))
    return count

#this function converts the number of moves into move score
# i.e moves = 0 => score = 0; moves = 1 score = 1, moves = 2 => score = 1+1/4 = 1.25, moves = 3 => score = 1 +1/4+1/9,etc
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
# geometric mean of quad_score and linear_score
mixed_score = [[linear_score[i][j]*quad_score[i][j] if linear_score[i][j] > 0 else -linear_score[i][j]*quad_score[i][j] for j in range(9)]for i in range (9)]

def custom_score(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return mixed_score[own_moves][opp_moves]

def custom_score_2(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return quad_score[own_moves][opp_moves]

def custom_score_3(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return linear_score[own_moves][opp_moves]
