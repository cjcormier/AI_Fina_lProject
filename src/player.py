from src.strategies import *
from src.logging import Log


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

        fascist_prob = self.num_fascists / (len(self.probabilities) - 1)
        hitler_prob = 1 / (len(self.probabilities) - 1)
        self.init_prob(known_roles, fascist_prob, hitler_prob, (0, 0))
        # if role is Role.FASCIST:
        #     self.init_prob(known_roles, 0, 0, (1, 0))
        # elif role is Role.LIBERAL:
        #     fascist_prob = self.num_fascists / (len(self.probabilities)-1)
        #     hitler_prob = 1 / (len(self.probabilities)-1)
        #     self.init_prob(known_roles, fascist_prob, hitler_prob, (0, 0))
        # elif role is Role.HITLER:
        #     if len(self.probabilities) > 6:
        #         fascist_prob = (self.num_fascists-1) / (len(self.probabilities)-1)
        #         self.init_prob(known_roles, fascist_prob, 0, (1, 1))
        #     else:
        #         self.init_prob(known_roles, 0, 0, (1, 1))

    def init_prob(self, known_roles, fascist_prob, hitler_prob, self_prob):
        self.fascists = known_roles[Role.FASCIST]
        self.hitler = known_roles[Role.HITLER]
        for player in self.probabilities:
            if player in self.fascists:
                self.probabilities[player] = (1, 0)
            elif player is self.name:
                self.probabilities[player] = self_prob
            elif player is self.hitler:
                self.probabilities[player] = (1, 1)
            else:
                self.probabilities[player] = (fascist_prob, hitler_prob)

    def set_prob(self, player, new_prob, new_hitler_prob=None):
        new_prob = clamp(new_prob, 0, 1)
        if new_hitler_prob is None:
            new_hitler_prob = self.probabilities[player][1]

        sub = 2
        if player in self.fascists:
            sub = 1
        change_prob = new_prob - self.probabilities[player][0]
        change_prob /= (len(self.probabilities) - len(self.fascists) - sub)

        self.probabilities[player] = (new_prob, new_hitler_prob)
        for curr_player in self.probabilities:
            if curr_player not in [self.name, player] and curr_player not in self.fascists:
                curr_prob = clamp(self.probabilities[curr_player][0] - change_prob, 0, 1)
                self.probabilities[curr_player] = (curr_prob, new_hitler_prob)

    def print_probs(self):
        Log.log('Player {} Probabilities:'.format(self.name))
        prob_fascist, prob_hitler = (0, 0)
        for n in self.probabilities:
            Log.log('\t{}: {}'.format(n, self.probabilities[n]))
            prob_fascist = prob_fascist+self.probabilities[n][0]
            prob_hitler = prob_hitler+self.probabilities[n][1]
        Log.log('Total: ({}, {})'.format(prob_fascist, prob_hitler))

    def set_strategy(self, strategy_type, strategy):
        self.strategies[strategy_type] = strategy

    def set_strategies(self, strategies):
        self.strategies = strategies

    def choose_chancellor(self, valid_players_names):
        return self.strategies[StrategyTypes.CHOOSE_CHANCELLOR](self, valid_players_names)

    def chancellor_pick(self, president_name, cards, deck):
        return self.strategies[StrategyTypes.CHANCELLOR_CARDS](self, president_name, cards, deck)

    def president_pick(self, chancellor_name, cards):
        cards = self.strategies[StrategyTypes.PRESIDENT_CARDS](self, chancellor_name, cards)
        return cards

    def vote(self, president_name, chancellor_name):
        return self.strategies[StrategyTypes.VOTE](self, chancellor_name, president_name)

    def analyze_vote(self, president_name, chancellor_name, votes):
        pass

    def analyze_revealed_card(self, chancellor, president, card, remaining):
        self.strategies[StrategyTypes.ANALYZE_REVEALED_CARD](self, chancellor, president,
                                                             card, remaining)

    def analyze_chancellor_card(self, chancellor, pres_card, chanc_card):
        self.strategies[StrategyTypes.ANALYZE_CHANCELLOR_CARD](self, chancellor, pres_card,
                                                               chanc_card)

    def shoot(self):
        return self.strategies[StrategyTypes.SHOOT](self)

    def remove_player(self, player):
        del self.probabilities[player]
        if player in self.fascists:
            self.fascists.remove(player)

    def max_fascist(self):
        probabilities = self.probabilities
        max_prob = 0
        max_player = None
        for player in probabilities:
            prob = probabilities[player][0]
            if prob > max_prob:
                max_player = player
                max_prob = prob
        return max_player

    def min_fascist(self):
        probabilities = self.probabilities
        min_prob = 1
        min_player = None
        for player in probabilities:
            prob = probabilities[player][0]
            if prob < min_prob:
                min_player = player
                min_prob = prob
        return min_player


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
