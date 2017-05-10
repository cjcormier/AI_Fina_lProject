from src.strategies import *
from src.logging import Log
from src.roles import Role


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

        if role is Role.FASCIST:
            self.init_prob(known_roles, 0, 0, (1, 0))
        elif role is Role.LIBERAL:
            self.init_prob(known_roles, fascist_prob, hitler_prob, (0, 0))
        elif role is Role.HITLER:
            if len(self.probabilities) > 6:
                fascist_prob = (self.num_fascists-1) / (len(self.probabilities)-1)
                self.init_prob(known_roles, fascist_prob, 0, (1, 1))
            else:
                self.init_prob(known_roles, 0, 0, (1, 1))

    def init_prob(self, known_roles, fascist_prob, hitler_prob, self_prob):
        fascist_prob = float(fascist_prob)
        hitler_prob = float(hitler_prob)
        self_prob = (float(self_prob[0]), float(self_prob[1]))

        self.fascists = known_roles[Role.FASCIST]
        self.hitler = known_roles[Role.HITLER]
        if known_roles[Role.HITLER] is not None:
            self.fascists += [known_roles[Role.HITLER]]
        for player in self.probabilities:
            if player in self.fascists:
                self.probabilities[player] = (1.0, 0.0)
            elif player is self.name:
                self.probabilities[player] = self_prob
            elif player is self.hitler:
                self.probabilities[player] = (1.0, 1.0)
            else:
                self.probabilities[player] = (fascist_prob, hitler_prob)

    def set_prob(self, player, new_prob, hitler_prob=None):
        # assert new_prob <= 1
        new_prob = float(new_prob)
        if new_prob != self.probabilities[player]:
            hitler_prob = hitler_prob if hitler_prob is not None else self.probabilities[player][1]
            self.probabilities[player] = (new_prob, hitler_prob)
            self.adjust_probs()

    def adjust_probs(self):
        sum_prob = sum([prob[0] for x, prob in self.probabilities.items() if x not in self.fascists])
        scale_factor = 1.0 if sum_prob == 0 else (self.num_fascists - len(self.fascists))/sum_prob

        recurse = False
        for curr_player, curr_probs in self.probabilities.items():
            if curr_player not in self.fascists:
                next_fascist_prob = curr_probs[0] * scale_factor
                self.probabilities[curr_player] = (next_fascist_prob, curr_probs[1])
        #         if next_fascist_prob > 1:
        #             recurse = True
        #             self.probabilities[curr_player] = (1.0, curr_probs[1])
        #             self.fascists.append(curr_player)
        # if recurse:
        #     self.adjust_probs()

    def print_probs(self):
        Log.log_probs('Player {} Probabilities:'.format(self.name))
        prob_fascist, prob_hitler = (0, 0)
        for n in self.probabilities:
            Log.log_probs('\t{0}: ({1[0]:.4}, {1[1]:.4})'.format(n, self.probabilities[n]))
            prob_fascist = prob_fascist+self.probabilities[n][0]
            prob_hitler = prob_hitler+self.probabilities[n][1]
        Log.log_probs('Total: ({0:.4}, {1:.4})'.format(prob_fascist, prob_hitler))

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

    def shoot(self, valid_players):
        return self.strategies[StrategyTypes.SHOOT](self, valid_players)

    def remove_player(self, player):
        # del self.probabilities[player]
        # if player in self.fascists:
        #     self.fascists.remove(player)
        pass

    def max_fascist(self, choices=None):
        probabilities = self.probabilities
        max_prob = 0
        max_player = None
        if choices is None:
            choices = probabilities
        for player in choices:
            prob = probabilities[player][0]
            if prob >= max_prob:
                max_player = player
                max_prob = prob
        return max_player

    def min_fascist(self, choices=None):
        probabilities = self.probabilities
        min_prob = 1
        min_player = None
        if choices is None:
            choices = probabilities
        for player in choices:
            prob = probabilities[player][0]
            if prob <= min_prob:
                min_player = player
                min_prob = prob
        return min_player


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

__all__ = ['Player']
