
# Build a Game-playing Agent

![Example game of isolation](viz.gif)

## Synopsis

This project was submitted as part of a requirement for Artificial Intelligence Nanodegree at Udacity
In this project, I developed an adversarial search agent to play the game "Isolation".  Isolation is a deterministic, two-player game of perfect information in which the players alternate turns moving a single piece from one cell to another on a board.  Whenever either player occupies a cell, that cell becomes blocked for the remainder of the game.  The first player with no remaining legal moves loses, and the opponent is declared the winner.  These rules are implemented in the `isolation.Board` class provided in the repository. 

This project uses a version of Isolation where each agent is restricted to L-shaped movements (like a knight in chess) on a rectangular grid (like a chess or checkerboard).  The agents can move to any open cell on the board that is 2-rows and 1-column or 2-columns and 1-row away from their current position on the board. Movements are blocked at the edges of the board (the board does not wrap around), however, the player can "jump" blocked or occupied spaces (just like a knight in chess).

Additionally, agents will have a fixed time limit each turn to search for the best move and respond.  If the time limit expires during a player's turn, that player forfeits the match, and the opponent wins.

Students only need to modify code in the `game_agent.py` file to complete the project.  Additional files include example Player and evaluation functions, the game board class, and a template to develop local unit tests.  


## Project Results
Most of the results can be found in "heuristic analysis.pdf"
In addition to implementing simple alpha-beta search and finding the best heuristics for the game, which can be seen as similar to a rule number of player moves - number of opponents moves, I also went beyond the requirement in implementing move ordering strategies, as well as symmetry calculations and optimized the internal working of the classes provided by the course that lead to a significant speed up of the agent.

You can also see a research review of AlphaGo game playing agent that won against human world champion in research_review.pdf


