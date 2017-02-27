from src.roles import *
from src.strategies import *
from src.info import *


class Player:
    def __init__(self, name, player_names, num_fascists):
        self.name = name
        self.role = None
        self.strategy = None
        self.fascists = []
        self.hitler = None
        self.num_fascists = num_fascists
        self.strategies = {}
        self.probabilities = {}
        for player_name in player_names:
            if player_name is not self.name:
                self.probabilities[player_name] = None

    def set_liberal(self):
        fascist_prob = self.num_fascists / (len(self.probabilities)-1)
        hitler_prob = 1 / (len(self.probabilities)-1)
        for player in self.probabilities:
            if player == self.name:
                self.probabilities[player] = (0, 0)
            else:
                self.probabilities[player] = (fascist_prob, hitler_prob)

    def set_role(self, role, known_roles):
        self.role = role

        if role is Role.FASCIST:
            self.init_prob(known_roles, 0, 0, (1, 0))
        elif role is Role.LIBERAL:
            fascist_prob = self.num_fascists / (len(self.probabilities)-1)
            hitler_prob = 1 / (len(self.probabilities)-1)
            self.init_prob(known_roles, fascist_prob, hitler_prob, (0, 0))
        elif role is Role.HITLER:
            if len(self.probabilities) > 6:
                fascist_prob = (self.num_fascists-1) / (len(self.probabilities)-1)
                self.init_prob(known_roles, fascist_prob, 0, (1, 1))
            else:
                self.init_prob(known_roles, 0, 0, (1, 1))

    def init_prob(self, known_roles, fascist_prob, hitler_prob, self_prob):
        self.fascists = known_roles[Role.FASCIST]
        self.hitler = known_roles[Role.FASCIST]
        for player in self.probabilities:
            if player in self.fascists:
                self.probabilities[player] = (1, 0)
            elif player is self.name:
                self.probabilities[player] = self_prob
            elif player is self.hitler:
                self.probabilities[player] = (1, 1)
            else:
                self.probabilities[player] = (fascist_prob, hitler_prob)

    def set_strategy(self, strategy_type, strategy):
        self.strategies[strategy_type] = strategy

    def choose_chancellor(self, valid_players):
        return self.strategies[Strategy_Types.CHOOSE_PRES](self, valid_players)

    def chancellor_pick(self, president, cards):
        return self.strategies[Strategy_Types.CHANCELLOR_CARDS](self, president, cards)

    def president_pick(self, chancellor, cards):
        cards, self.probabilities = self.strategies[Strategy_Types.PRESIDENT_CARDS](self, chancellor, cards)
        return cards

    def vote(self, president, chancellor):
        return self.strategies[Strategy_Types.VOTE](self, chancellor, president)

    def analyze_vote(self, president, chancellor, votes):
        pass

    def analyze_revealed_card(self, chancellor, president, card):
        self.strategies[Strategy_Types.ANALYZE_REVEALED_CARD](self, chancellor, president, card)
