from random import shuffle
#import numpy as np
import matplotlib.pyplot as plt
#from mpl.toolkists.axes_grid.axislines import SubplotZero
shoe = []
discard = []

BLACKJACK_PAYOUT = 1.2
DECKS_IN_SHOE = 8
START_CHIPS = 100000
                            # 2    3    4    5    6    7    8    9    10   ace
dealer_hits_soft_17 = [ [0,0,'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h', 'h' ], # 5-8   0
                        [0,0,'h','dd','dd','dd','dd', 'h', 'h', 'h', 'h', 'h' ], # 9     1
                        [0,0,'dd','dd','dd','dd','dd','dd','dd','dd','h', 'h' ], # 10    2
                        [0,0,'dd','dd','dd','dd','dd','dd','dd','dd','dd','dd'], # 11    3
                        [0,0,'h', 'h', 's', 's', 's', 'h', 'h', 'h', 'h', 'h' ], # 12    4
                        [0,0,'s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h' ], # 13    5
                        [0,0,'s', 's', 's', 's', 's', 'h', 'h', 'h', 'h', 'h' ], # 14    6
                        [0,0,'s', 's', 's', 's', 's', 'h', 'h', 'h', 'sr','sr'], # 15    7  
                        [0,0,'s', 's', 's', 's', 's', 'h', 'h', 'sr','sr','sr'], # 16    8
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 'sr'], # 17    9
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 's' ], # 18    10
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 's' ], # 19    11
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 's' ], # 20    12
                        [0,0,'h', 'h', 'h', 'dd','dd','h', 'h', 'h', 'h', 'h' ], # A2    13
                        [0,0,'h', 'h', 'h', 'dd','dd','h', 'h', 'h', 'h', 'h' ], # A3    14
                        [0,0,'h', 'h','dd', 'dd','dd','h', 'h', 'h', 'h', 'h' ], # A4    15
                        [0,0,'h', 'h','dd', 'dd','dd','h', 'h', 'h', 'h', 'h' ], # A5    16
                        [0,0,'h', 'dd','dd','dd','dd','h', 'h', 'h', 'h', 'h' ], # A6    17
                        [0,0,'dd','dd','dd','dd','dd','s', 's', 'h', 'h', 'h' ], # A7    18
                        [0,0,'s', 's', 's', 's', 'dd','s', 's', 's', 's', 's' ], # A8    19
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 's' ], # A9    20
                        [0,0,'sp','sp','sp','sp','sp','sp','h', 'h', 'h', 'h' ], # 2s    21
                        [0,0,'sp','sp','sp','sp','sp','sp','h', 'h', 'h', 'h' ], # 3s    22
                        [0,0,'h', 'h', 'h', 'sp','sp','h', 'h', 'h', 'h', 'h' ], # 4s    23
                        [0,0,'dd','dd','dd','dd','dd','dd','dd','dd','h', 'h' ], # 5s    24
                        [0,0,'sp','sp','sp','sp','sp','h', 'h', 'h', 'h', 'h' ], # 6s    25
                        [0,0,'sp','sp','sp','sp','sp','sp','h', 'h', 'h', 'h' ], # 7s    26
                        [0,0,'sp','sp','sp','sp','sp','sp','sp','sp','sp','sr'], # 8s    27
                        [0,0,'sp','sp','sp','sp','dd','s', 'sp','sp','s', 's' ], # 9s    28
                        [0,0,'s', 's', 's', 's', 's', 's', 's', 's', 's', 's' ], # 10s   29
                        [0,0,'sp','sp','sp','sp','sp','sp','sp','sp','sp','sp'], # As    30
                             ]

def add_deck_to_shoe():
    for suit in ['s','h','d','c']:
        for card in ['A',2,3,4,5,6,7,8,9,10,'J','Q','K']:
            shoe.append([card, suit])

class Player:

    def __init__(self, name):
        self.chips = START_CHIPS
        self.hands = []
        self.name = str(name)
        self.history = []
        self.history.append(self.chips)

    def action(self, h, strat, dealer):
        #print '********************** Bet:', h.bet
        move = ""
        if h.has_blackjack():
            h.status = "blackjack"
        else:
            while not (move == "s" or h.status == "bust"):
                # Find value of dealer's face up card
                dealer_val = card_to_val(dealer.hands[0].cards[0][0])

                # If player has a pair
                if h.cards[0][0] == h.cards[1][0]:
                    move = strat[card_to_val(h.cards[0][0])+19][dealer_val]
                # If a player has a "soft" total
                elif h.sum()[1]:
                    try:
                        move = strat[h.sum()[0]][dealer_val]
                    except IndexError:
                        print "~~~~~"
                        print h.sum()[0]-8, dealer_val
                        print h.print_hand()
                        print "~~~~~"
                # Otherwise, just with just a regular total
                else:
                    if h.sum()[0] <= 8:
                        move = strat[0][dealer_val]
                    else:
                        try:
                            move = strat[h.sum()[0]-8][dealer_val]
                        except IndexError:
                            print "~~~~~"
                            print h.sum()[0]-8, dealer_val
                            h.print_hand()
                            print "~~~~~"
                            

                # Can't double or surrender with more than 2 cards
                if (move == "dd" and len(h.cards) > 2) or (move == "sr" and len(h.cards) > 2):
                    move = "h"
                # Can't split with more than 2 cards
                if move == "sp" and len(h.cards) > 2:
                    # If a player has a "soft" total
                    if h.sum()[1]:
                        move = strat[h.sum()[0]][dealer_val]
                    # Otherwise, just with just a regular total
                    else:
                        if h.sum()[0] <= 8:
                            move = strat[0][dealer_val]
                        else:
                            move = strat[h.sum()[0]-8][dealer_val]                 
                    
                if move == "dd":
                    #print "DOUBLING"
                    h.bet += self.bet(h.bet)
                    h.hit()
                elif move == "sp":
                    #print "SPLITTING"
                    new_h = Hand(self.bet(h.bet))
                    new_h.cards = [h.cards.pop()]
                    print "NEW_H", new_h
                    self.hands.append(new_h)
                    self.hands[0].hit()
                    self.hands[1].hit()
                    self.action(self.hands[0], strat, dealer)
                    print "HANDS LEN:", len(self.hands)
                    if len(self.hands) > 4:
                        for hn in self.hands:
                            print "@@@@@@"
                            hn.print_hand()
                    self.action(self.hands[1], strat, dealer)
                elif move == "sr":
                    #print "SURRENDERING"
                    self.chips += h.bet * .5
                    self.hands = list(set(self.hands) - set([h]))
                    #print "loser", self.name, self.chips
                    move = "s"
                elif move == "h":
                    #print "HITTING"
                    h.hit()
                elif move == "s":
                    #print "STAYING"
                    pass
                    
                if h.sum()[0] > 21:
                    h.status = "bust"
                if h.sum()[0] == 21:
                    move == "s"
        
        if not move == "sp":
            #h.print_hand()
            #print "total: ", h.sum()[0]
            pass

    def bet(self, bet):
        if self.chips <= 0:
            #print "BANKRUPT"
            pass
        else:
            self.chips = self.chips - bet
            return bet

    def bet_and_reset(self):
        self.hands = [Hand(self.bet(5))]

class Hand:
    
    def __init__(self, bet):
        self.cards = []
        self.status = "pending" # pending, win, lose, blackjack, bust, push
        self.bet = bet

    def hit(self):
        self.cards.append(shoe.pop())

    def has_blackjack(self):
        if self.sum()[0] == 21 and len(self.cards) == 2:
            return True
        else:
            return False

    def sum(self):
        total = 0
        soft = False
        had_ace = False
        for card in self.cards:
            if isinstance(card[0], int):
                total = card[0] + total
            else:
                if card[0] == 'A' and not had_ace:
                    total = 11 + total
                    had_ace = True
                    soft = True
                elif card[0] == 'A' and had_ace:
                    total = 1 + total
                elif card[0] == 'K' or card[0] == 'Q' or card[0] == 'J':
                    total = 10 + total
        if soft and total > 21:
            total = total - 10
        return [total, soft]

    def print_hand(self):
        for card in self.cards:
            print str(card[0]) + card[1]

class Dealer(Player):

    def __init__(self, name):
        Player.__init__(self, name)

    def action(self, h, strat, dealer):
        #print "**********************"
        if h.has_blackjack():
            h.status = "blackjack"
        else:
            while h.sum()[0] < 17:
                h.hit()
            if h.sum()[0] > 21:
                h.status = "bust"

        #h.print_hand()
        #print "total: ", h.sum()[0]

class Counter:

    def __init__(self, strat, threshold):
        self.strat = strat
        self.threshold = threshold
        self.count = 0

    def tally(self, card):
        self.count += strat[card_to_val(card)]

    def reset_count(self):
        self.count = 0

    def is_hot(self):
        if self.count > self.threshold:
            return True

class Game:

    def __init__(self, num_players):
        self.Players = []
        for i in range(num_players):
            self.Players.append(Player(i+1))
        self.Players.append(Dealer("Dealer"))

    def deal_table(self):
        for i in range(2):
            for p in self.Players:
                p.hands[0].hit()

    def find_winners(self):
        if self.Players[-1].hands[0].status == 'blackjack':
            for p in self.Players[:-1]:
                for h in p.hands:
                    h.status = "lose"
        else:
            for p in self.Players[:-1]:
                for h in p.hands:
                    if h.status == "pending":
                        if h.sum()[0] > 21:         # gotta check for that bust again
                            h.status = "bust"
                        elif self.Players[-1].hands[0].status == "bust":
                            h.status = "win"
                        elif h.sum()[0] > self.Players[-1].hands[0].sum()[0]:
                            h.status = "win"
                        elif h.sum()[0] == self.Players[-1].hands[0].sum()[0]:
                            h.status = "push"
                        elif h.sum()[0] < self.Players[-1].hands[0].sum()[0]:
                            h.status = "lose"

    def resolve_bets(self):
        #print "~~~~~~~~~~~~~~~~~~~~~"
        for p in self.Players[:-1]:
            for h in p.hands:
                if h.status == "win":
                    p.chips += h.bet + h.bet
                    #print "winner", p.name, p.chips
                elif h.status == "lose" or h.status == "bust":
                    #print "loser", p.name, p.chips
                    pass
                elif h.status == "push":
                    p.chips += h.bet
                    #print "pusher", p.name, p.chips
                elif h.status == "blackjack":
                    p.chips += h.bet + (h.bet * BLACKJACK_PAYOUT)
                    #print "BLACKJACKER", p.name, p.chips

    def discard_hands(self):
        for p in self.Players:
            for h in p.hands:
                for crd in h.cards:
                    discard.append(crd)

    def round(self):
        global shoe
        global discard
        if len(shoe) < 50:
            shoe = []
            discard = []
            for i in range(DECKS_IN_SHOE):
                add_deck_to_shoe()
            shuffle(shoe)
            
        for p in self.Players:
            p.bet_and_reset()
        self.deal_table()
        if not self.Players[-1].hands[0].has_blackjack():
            for p in self.Players:
                #print "###################### Player:", p.name
                p.action(p.hands[0], dealer_hits_soft_17, self.Players[-1])
        else:
            #print "Goddamn dealer got blackjack"
            pass
        self.find_winners()
        self.resolve_bets()
        for p in self.Players[:-1]:
            p.history.append(p.chips)
        self.discard_hands()

    def graph_history(self):
        args = []
        moves = range(len(self.Players[0].history))
        args.append(moves)
        args.append([START_CHIPS]*len(moves))
        for p in self.Players[:-1]:
            args.append(moves)
            args.append(p.history)
        plt.plot(*args)
        plt.show()

# Takes the actual first element of a card tuple
def card_to_val(card):
        if isinstance(card, int):
            return card
        if card == "K" or card == "Q" or card == "J":
            return 10
        elif card == "A":
            return 11
            

g = Game(4)
g.round()
def go():
    g.round()

    
