TIME_LIMIT = 150
import random
from isolation import Board
from sample_players import *
from game_agent import *
import timeit

time_limit = 1000
time_millis = lambda: 1000 * timeit.default_timer()
def play_round(player1, player2, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    stats = [0]*47
    depth = [0]*47

    for _ in range(num_matches):

        game =Board(player1, player2)


        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(game.get_legal_moves())
            print (move)
            game.apply_move(move)

        # play all games and tally the results
        turnCounter = 0
        while True:

            print (turnCounter)
            legal_player_moves = game.get_legal_moves()
            game_copy = game.copy()

            move_start = time_millis()
            print (move_start)
            time_left = lambda: time_limit - (time_millis() - move_start)
            print (time_left())

            curr_move = game.active_player.get_move(game_copy, time_left)
            print (curr_move)

            if curr_move is None:
                curr_move = Board.NOT_MOVED

            if curr_move not in legal_player_moves:
                break

            stats[turnCounter] += (len (legal_player_moves)/num_matches)
            #depth[turnCounter] += (game.active_player.depth/num_matches)
            #print (game.active_player.depth)
            turnCounter +=1
            game.apply_move(curr_move)

    return stats,depth


player1 = HumanPlayer()
player2 = AlphaBetaPlayer()
stats,depth = play_round(player1, player2, 1)
with open('alpha.txt', 'w') as file_handler:
    for item in stats:
        file_handler.write("{}\n".format(item))