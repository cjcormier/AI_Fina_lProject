"""Contains the classes for the players."""
from typing import *

from secret_hitler_ai.role import Role, Prob, RoleProbs
from secret_hitler_ai.strategytypes import StrategyTypes as St

Name = Union[str, int]


class Player:
    """Contains information and classes about the player."""
    def __init__(self, name: Name, player_names: List[Name], num_fascists: int):
        self.name = name
        self.role = None
        self.fascists: List[Name] = []
        self.hitler = None
        self.num_fascists = num_fascists
        self.strats: Dict[St, Callable[..., ...]] = {}
        self.probabilities: Dict[Name, RoleProbs] = {}
        self.initial_probs: RoleProbs = RoleProbs(0, 0)
        for player_name in player_names:
            self.probabilities[player_name] = RoleProbs(0, 0)

    def set_roles(self, role: Role, known_roles: Dict[Role, List[Name]]):
        """Sets the role of the player as well as the known roles of the other players.
        This should be invoked only before the start of the game.
        
        :param role: The Role of the player.
        :param known_roles: The roles that the player knows.
        """
        self.role = role
        num_others = len(self.probabilities)-1

        if role is Role.FASCIST:
            self.initial_probs = RoleProbs(0, 0)
            self.initialize_prob(known_roles, RoleProbs(1, 0))
        elif role is Role.LIBERAL:
            fascist_prob = self.num_fascists / (len(self.probabilities) - 1)
            hitler_prob = 1 / (len(self.probabilities) - 1)
            self.initial_probs = RoleProbs(fascist_prob, hitler_prob)
            self.initialize_prob(known_roles, RoleProbs(0, 0))
        elif role is Role.HITLER:
            if len(self.probabilities) > 6:
                fascist_prob = (self.num_fascists-1) / (len(self.probabilities)-1)
                self.initial_probs = RoleProbs(fascist_prob, 0)
            else:
                self.initial_probs = RoleProbs(0, 0)
            self.initialize_prob(known_roles, RoleProbs(1, 1))

    def initialize_prob(self, known_roles: Dict[Role, List[Name]],
                        self_prob: RoleProbs):
        """Initializes the probabilities for the other players.
        
        :param known_roles: The known roles.
        :param self_prob: The probability that 
        """
        fascist_prob = self.initial_probs.fascist
        hitler_prob = self.initial_probs.hitler

        self.fascists = known_roles[Role.FASCIST]
        self.hitler = known_roles[Role.HITLER]
        if known_roles[Role.HITLER] is not None:
            self.fascists += [known_roles[Role.HITLER]]
        for player in self.probabilities:
            if player in self.fascists:
                self.probabilities[player] = RoleProbs(1, 0)
            elif player is self.name:
                self.probabilities[player] = self_prob
            elif player is self.hitler:
                self.probabilities[player] = RoleProbs(1, 1)
            else:
                self.probabilities[player] = RoleProbs(fascist_prob, hitler_prob)

    def set_prob(self, player, fascist_prob: Prob):
        """Sets the probability for the given player.
        
        :param player: Player to set the new probabilities.
        :param fascist_prob: The new fascist probability.
        """
        fascist_prob = fascist_prob
        if fascist_prob != self.probabilities[player].fascist:
            self.probabilities[player].fascist = fascist_prob
            self.adjust_probs()

    def adjust_probs(self):
        """
        Adjusts the probability table so that it stays within the proper bounds
        """
        sum_prob = sum([prob.fascist for x, prob in self.probabilities.items() if x not in self.fascists])
        scale_factor = 1.0 if sum_prob == 0 else (self.num_fascists - len(self.fascists))/sum_prob

        # recurse = False
        for curr_player, curr_probs in self.probabilities.items():
            if curr_player not in self.fascists:
                curr_probs.fascist *= scale_factor
        #         if next_fascist_prob > 1:
        #             recurse = True
        #             self.probabilities[curr_player] = RoleProbs(1, curr_probs[1])
        #             self.fascists.append(curr_player)
        # if recurse:
        #     self.adjust_probs()

    def set_strategy(self, strategy_type, strategy):
        self.strats[strategy_type] = strategy

    def set_strategies(self, strategies):
        self.strats.update(strategies)

    def choose_chancellor(self, valid_players_names):
        return self.strats[St.CHOOSE_CHANCELLOR](self, valid_players_names)

    def chancellor_pick(self, president_name, cards, deck):
        return self.strats[St.CHANCELLOR_CARDS](self, president_name, cards, deck)

    def president_pick(self, chancellor_name, cards):
        cards = self.strats[St.PRESIDENT_CARDS](self, chancellor_name, cards)
        return cards

    def vote(self, president_name, chancellor_name):
        return self.strats[St.VOTE](self, chancellor_name, president_name)

    def analyze_vote(self, president_name, chancellor_name, votes):
        pass

    def analyze_revealed_card(self, chancellor, president, card, remaining):
        self.strats[St.ANALYZE_REVEALED_CARD](self, chancellor, president, card, remaining)

    def analyze_chancellor_card(self, chancellor, pres_card, chanc_card):
        self.strats[St.ANALYZE_CHANCELLOR_CARD](self, chancellor, pres_card, chanc_card)

    def shoot(self, valid_players):
        return self.strats[St.SHOOT](self, valid_players)

    def remove_player(self, player: Name):
        """Remove a player that has been shot. :class:`role.Role`
        
        :param player: Player to remove.
        """
        # del self.probabilities[player]
        # if player in self.fascists:
        #     self.fascists.remove(player)
        pass

    def max_fascist(self, choices: List[Name]=list())->Name:
        """Return the player who is most likely to be fascist.
        
        :param choices: The list of valid players to choose from, empty list implies all 
            players are valid.
        :return: The player who is most likely to be fascist.
        """
        probabilities = self.probabilities
        max_prob = 0
        max_player = None
        if len(choices) == 0:
            choices = self.probabilities.keys()
        for player in choices:
            prob = probabilities[player].fascist
            if prob >= max_prob:
                max_player = player
                max_prob = prob
        return max_player

    def min_fascist(self, choices:  List[Name]=list())->Name:
        """Return the player who is least likely to be fascist.
        
        :param choices: The list of valid players to choose from, empty list implies all 
            players are valid.
        :return: The player who is least likely to be fascist.
        """
        probabilities = self.probabilities
        min_prob = 1
        min_player = None
        if len(choices) == 0:
            choices = probabilities
        for player in choices:
            prob = probabilities[player].fascist
            if prob <= min_prob:
                min_player = player
                min_prob = prob
        return min_player

__all__ = ['Player']
