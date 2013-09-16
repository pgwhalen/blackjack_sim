Blackjack Sim
=============

Born out of a four hour, combinatorics-laden discussion I had with a friend while waiting for our plane home after my first weekend in Vegas, I wanted to write a simple simulation of blackjack that could be tweaked in a number of ways to see how various strategies and modifications of the game would fare for the player.

In its current state, it simulates the game and shows a chart of the players' money over time, but the players lose money faster than I would expect, so I suspect there is a bug.  Verifying that the game is played correctly is the first priority, other todos include

- [] finish Counter (card counter) class so that a player may be influenced by various counting strategies
- [] implement some sort of side bet feature, so typical side bets can be incorporated in a player's strategy

Dependencies
------------
MatPlotLib - only necessary to show graphs obviously, otherwise the script should run standalone.