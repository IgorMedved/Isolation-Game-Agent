"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings
import multiprocessing

from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, GreedyPlayer, ImprovedPlayer, open_move_score,
                            improved_score, center_score, open_move_score_mod, improved_score_mod, improved_score_sym)
from game_agent import (MinimaxPlayer, #AlphaBetaPlayerPartialSort, AlphaBetaPlayerNoSort, AlphaBetaPlayerFullSort,
                        #AlphaBetaPlayerPartialSort1, AlphaBetaPlayerPartialSortDeep,custom_score, greedy_endgame_score,
                        #AlphaBetaPlayerPartialSort2, AlphaBetaPlayerPartialSort3, AlphaBetaPlayer,
                        AlphaBetaPlayer, custom_score, AlphaBetaPlayer1,
                        custom_score_2, custom_score_3,custom_score_4,custom_score_5, custom_score61, custom_score62,
                        custom_score63, custom_score64, custom_score65, custom_score66, custom_score68,custom_score69,
                        custom_score67, custom_score611,custom_score612,custom_score613,custom_score614, custom_score615, custom_score616)

NUM_MATCHES = 10000 # number of matches against each opponent
TIME_LIMIT = 1000  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                     #Board(cpu_agent.player, agent.player, 7,7)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            #move = random.choice(games[0].get_legal_moves())
            if _ == 0:
                move = (0,0)
            else:
                move = (5,5)
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, _, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

            if termination == "timeout":
                timeout_count += 1
            elif termination == "forfeit":
                forfeit_count += 1

    return timeout_count, forfeit_count


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches):
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)
    numprocs = multiprocessing.cpu_count()-1

    print("\n{:^9}{:^13}".format("Match #", "Opponent") + ''.join(['{:^13}'.format(x[1].name) for x in enumerate(test_agents)]))
    print("{:^9}{:^13} ".format("", "") +  ' '.join(['{:^5}| {:^5}'.format("Won", "Lost") for x in enumerate(test_agents)]))

    for idx, agent in enumerate(cpu_agents):
        wins = {key: 0 for (key, value) in test_agents}
        wins[agent.player] = 0

        print("{!s:^9}{:^13}".format(idx + 1, agent.name), end="", flush=True)

        counts = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += counts[0]
        total_forfeits += counts[1]
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        print(' ' + ' '.join([
            '{:^5}| {:^5}'.format(
                round_totals[i],round_totals[i+1]
            ) for i in range(0, len(round_totals), 2)
        ]))

    print("-" * 74)
    print('{:^9}{:^13}'.format("", "Win Rate:") +
        ''.join([
            '{:^13}'.format(
                "{:.1f}%".format(100 * total_wins[x[1].player] / total_matches)
            ) for x in enumerate(test_agents)
    ]))

    if total_timeouts:
        print(("\nThere were {} timeouts during the tournament -- make sure " +
               "your agent handles search timeout correctly, and consider " +
               "increasing the timeout margin for your agent.\n").format(
            total_timeouts))
    if total_forfeits:
        print(("\nYour ID search forfeited {} games while there were still " +
               "legal moves available to play.\n").format(total_forfeits))


def main():

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = [
        #Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved"),
        #Agent(AlphaBetaPlayer(score_fn=custom_score), "AB_Custom"),
        #Agent(AlphaBetaPlayer(score_fn=custom_score_2), "AB_Custom_2"),
        #Agent(AlphaBetaPlayer(score_fn=custom_score_3), "AB_Custom_3")
        #Agent(RandomPlayer(), "RandomTest"),
        #Agent(GreedyPlayer(), "GreedyTest"),
        #Agent(ImprovedPlayer(), "ImprovedTest"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=improved_score), "ab3ps1_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=open_move_score), "ab3ps1_open"),
        #Agent(AlphaBetaPlayerPartialSort3(search_depth=3, score_fn=greedy_endgame_score), "ab3ps3_greedyend"),
        #Agent(AlphaBetaPlayerPartialSort3(search_depth=5, score_fn=greedy_endgame_score), "ab5ps3_greedyend")
        #Agent(AlphaBetaPlayer1(search_depth=1, score_fn=open_move_score), "greedy_ab1"),
        #Agent(AlphaBetaPlayer1(search_depth=1, score_fn=improved_score), "improved_ab1"),
        Agent(AlphaBetaPlayer1(search_depth=3, score_fn=open_move_score), "greedy_ab3"),
        #Agent(AlphaBetaPlayer1(search_depth=7, score_fn=improved_score), "improved_ab7"),
        #Agent(AlphaBetaPlayer1(search_depth=3, score_fn=custom_score), "mixed_ab3"),
        #Agent(AlphaBetaPlayer1(search_depth=3, score_fn=custom_score_3), "linear_ab3"),
        #Agent(AlphaBetaPlayer1(search_depth=7, score_fn=open_move_score), "greedy_ab7"),
        #Agent(AlphaBetaPlayer1(search_depth=5, score_fn=improved_score), "improved_ab5"),

        #Agent(AlphaBetaPlayer1(search_depth=5, score_fn=custom_score_3), "ab5_linear")

        #Agent(ImprovedPlayer(), "ImprovedTest")
        #Agent(ImprovedPlayer(score_fn=improved_score_mod), "Improved_Center"),
        #Agent(MinimaxPlayer(search_depth=2, score_fn=open_move_score), "MM2_Open"),
        #Agent(MinimaxPlayer(search_depth=2, score_fn=improved_score), "MM2_Improved"),
        #Agent(MinimaxPlayer(search_depth=2, score_fn=improved_score_mod), "MM2_Improved_Center")
        #Agent(MinimaxPlayer(search_depth=3, score_fn=open_move_score), "MM3_Open"),
        #Agent(MinimaxPlayer(search_depth=3, score_fn=improved_score), "MM3_Improved"),
        #Agent(MinimaxPlayer(search_depth=3, score_fn=improved_score_mod), "MM3_Improved_Center")
        #Agent(MinimaxPlayer(search_depth=2, score_fn=open_move_score), "MM2_Open"),
        #Agent(MinimaxPlayer(search_depth=2, score_fn=improved_score), "MM2_Improved"),
        #Agent(MinimaxPlayer(search_depth=2, score_fn=improved_score_mod), "MM2_Improved_Center")
        #Agent(RandomPlayer(), "RandomTest"),
        #Agent(GreedyPlayer(), "GreedyTest")
        #Agent(MinimaxPlayer(search_depth=1, score_fn=improved_score), "MM1")
        #Agent(ImprovedPlayer(), "ImprovedTest")
        #Agent(MinimaxPlayer(search_depth=4, score_fn=open_move_score), "MM4_Open"),
        #Agent(MinimaxPlayer(search_depth=4, score_fn=improved_score), "MM4_Improved"),
        #Agent(MinimaxPlayer(search_depth=4, score_fn=improved_score_mod), "MM4_Improved_Center")

    ]

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        #Agent(RandomPlayer(), "Random"),
        #Agent(GreedyPlayer(), "Greedy"),
        #Agent(ImprovedPlayer(),"Improved"),
        #Agent(GreedyPlayer(score_fn=open_move_score_mod), "Greedy_Center"),
        #Agent(ImprovedPlayer(score_fn=improved_score_mod), "Improved_Center"),
        #Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        #Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        #Agent(MinimaxPlayer(score_fn=open_move_score_mod), "MM_Open_Center"),
        #Agent(MinimaxPlayer(score_fn=improved_score_mod), "MM_Improved_Center")

        #Agent(MinimaxPlayer(search_depth=5,score_fn=open_move_score), "MM5_Open"),
        #Agent(MinimaxPlayer(search_depth=5,score_fn=improved_score), "MM5_Improved")
        #Agent(MinimaxPlayer(search_depth=5, score_fn=improved_score_mod), "MM5_Improved_Center")
        #Agent(MinimaxPlayer(search_depth=3, score_fn=open_move_score), "MM3_Open"),
        #Agent(MinimaxPlayer(search_depth=3, score_fn=improved_score), "MM3_Improved"),
        #Agent(MinimaxPlayer(search_depth=3, score_fn=improved_score_mod), "MM3_Improved_Center")

        #Agent(MinimaxPlayer(search_depth=2, score_fn=improved_score), "MM2_Improved"),
        #Agent(MinimaxPlayer(search_depth=3, score_fn=improved_score), "MM3_Improved"),
        #Agent(MinimaxPlayer(search_depth=4, score_fn=improved_score), "MM4_Improved"),
        #Agent(AlphaBetaPlayerNoSort(search_depth=5, score_fn=improved_score), "ABNS5_Improved"),

        #Agent(AlphaBetaPlayerNoSort(search_depth=9, score_fn=improved_score), "ab9ns_Improved"),
        #Agent(AlphaBetaPlayerFullSort(search_depth=9, score_fn=improved_score), "ab9fs_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=open_move_score), "ab5ps1_open"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=improved_score), "ab5pss1_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=7, score_fn=custom_score_3), "ab7ps1_linear"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=7, score_fn=custom_score_4), "ab7ps1_quad"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=7, score_fn=custom_score_5), "ab7ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=improved_score), "ab5pss1_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score_3), "ab5ps1_linear"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score_4), "ab5ps1_quad"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score_5), "ab5ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=improved_score), "ab3pss1_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=custom_score_3), "ab3ps1_linear"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=custom_score_4), "ab3ps1_quad"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=3, score_fn=custom_score_5), "ab3ps1_mixed")
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score61), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score62), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score63), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score64), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score65), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score66), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score67), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score68), "ab561ps1_mixed"),
        #Agent(AlphaBetaPlayer1(search_depth=3, score_fn=custom_score), "mixed_ab3"),
        #Agent(AlphaBetaPlayer1(search_depth=3, score_fn=custom_score_2), "quad_ab3"),
        #Agent(AlphaBetaPlayer1(search_depth=7, score_fn=custom_score_3), "linear_ab7"),
        Agent(AlphaBetaPlayer1(search_depth=3, score_fn=improved_score), "improved_ab3"),
        #Agent(AlphaBetaPlayerPartialSort3(search_depth=3, score_fn=improved_score), "ab3ps1_improved"),
        #Agent(AlphaBetaPlayerPartialSort3(search_depth=5, score_fn=improved_score), "ab5ps2_improved"),
        #Agent(AlphaBetaPlayerPartialSort3(search_depth=5, score_fn=improved_score), "ab7ps3_improved"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score611), "ab56125ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score612), "ab5615ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score613), "ab56175ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score614), "ab562ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score615), "ab5601ps1_mixed"),
        #Agent(AlphaBetaPlayerPartialSort1(search_depth=5, score_fn=custom_score616), "ab56100ps1_mixed"),
        #Agent(GreedyPlayer(), "GreedyTest")
        #Agent(AlphaBetaPlayerPartialSortDeep(search_depth=3, score_fn=improved_score), "ab7pss1_improved"),
        #Agent(AlphaBetaPlayerPartialSort(search_depth=9, score_fn=improved_score), "ab9ps_Improved"),
        #Agent(AlphaBetaPlayerPartialSort(search_depth=3, score_fn=open_move_score_mod), "ab3_open_c"),
        #Agent(AlphaBetaPlayerPartialSort(search_depth=3, score_fn=improved_score_mod), "ab3_Improved_c"),
        #Agent(AlphaBetaPlayerNoSort(search_depth=3,score_fn=open_move_score), "AB3_Open"),

        #Agent(AlphaBetaPlayerNoSort(search_depth=3, score_fn=improved_score), "AB3_Improved"),
        #Agent(AlphaBetaPlayerNoSort(search_depth=3, score_fn=open_move_score_mod), "AB3_Open_c"),
        #Agent(AlphaBetaPlayerNoSort(search_depth=3, score_fn=improved_score_mod), "AB3_improved_c"),
    ]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))
    play_matches(cpu_agents, test_agents, NUM_MATCHES)


if __name__ == "__main__":
    main()
