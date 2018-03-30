"""Contains the class for running the game."""
from random import shuffle
from typing import Tuple, Dict

from secret_hitler_ai.board import BoardStates, Board
from secret_hitler_ai.deck import Deck, Card
from secret_hitler_ai.logging import Log
from secret_hitler_ai.player import Player, Name
from secret_hitler_ai.role import Role


class Game:
    """Class for running the game"""

    def __init__(self, num_players: int, allow_shoots: bool=False, log: Log=Log()):
        """ Constructor for the game class.

        Creates players as determined by the num_players argument. The strategies must
        be set after creation.

        :param num_players: Number of players
        :param allow_shoots: Determines if the shooting action is allowed
        :param log: The log to record actions.
        """
        self.num_players = num_players
        self.players = self.create_players(num_players)
        self.orig_players = dict(self.players)
        self.allow_shoots = allow_shoots
        self.board = Board()
        self.deck = Deck(6, 11)
        self.winner = BoardStates.NORMAL
        self.log = log

        self.prev_pres = -1
        self.president_name = -1
        self.president = None
        self.chancellor = None
        self.anarchies = 0

    def run(self) -> Tuple[BoardStates, int, int, int]:
        """Runs a full game"""
        rounds = 0
        Log.log('ROLES')
        for player in self.players.values():
            Log.log('{}: {}', (player.name, player.role))
        while self.winner is BoardStates.NORMAL:
            rounds += 1
            Log.log_new_round()
            self.round()
        self.log.log_game_results(rounds)

        return (self.winner, self.board.fascist_board,
                self.board.liberal_board, self.anarchies)

    def round(self) -> None:
        """Runs a singular round of the game"""
        if self.elect_new_gov():
            self.log.record_gov(self.president, self.chancellor)
            self.prev_pres = self.president_name
            if self.check_hitler_chanc_win():
                return
            remaining = self.deck.total_remaining()
            next_policy = self.enact_policy(remaining)
            self.analyze_revealed_card(next_policy, remaining)
        else:
            next_policy = self.deck.draw()
            self.anarchies += 1
            Log.log_anarchy()
        self.winner = self.board.increment_board(next_policy)
        Log.log_next_policy(next_policy)
        self.shoot(next_policy)
        Log.log_all_probs(self.players, self.orig_players)

    def elect_new_gov(self) -> bool:
        """Attempts to elect a government.

        If a vote fails, the turn moves to the next president and tries again.
        Fails to elect a government after three failed attempts

        :return: If the vote has passed."""
        rounds_of_voting = 0
        vote_passed = False

        # until the vote passes or 3 votes fail
        while not vote_passed and rounds_of_voting < 3:
            rounds_of_voting += 1
            self.next_pres()
            self.president, self.chancellor = self.propose_gov()

            vote_passed = self.vote()
            Log.log_vote_results(vote_passed, rounds_of_voting)
        return vote_passed

    def next_pres(self) -> None:
        """Determines the next president,

        NOTE: this currently only works when the players are the integers from 0 to
        the number of players"""
        # TODO actually get next pres from list
        self.president_name = (self.president_name + 1) % self.num_players
        while self.president_name not in self.players.keys():
            self.president_name = (self.president_name + 1) % self.num_players

    def propose_gov(self) -> Tuple[Player, Player]:
        """The next president chooses a chancellor and proposes that government.

        :return: The proposed president and chancellor."""
        players = self.players.keys()
        chancellor_name = self.chancellor.name if self.chancellor is not None else -1

        names = [x for x in players if x not in [chancellor_name, self.president_name]]
        if len(self.players) > 5:
            names = [x for x in names if x is not self.prev_pres]
        Log.log_valid_chancellors(names)

        president = self.players[self.president_name]
        chancellor_name = president.choose_chancellor(names)
        chancellor = self.players[chancellor_name]
        assert president is not chancellor
        return president, chancellor

    def check_hitler_chanc_win(self) -> bool:
        """Checks if the elected chancellor is hitler and if the fascists have won.

        Also sets the board state appropriatly

        :return: If the fascists won via Hitler being elected."""
        Log.log_elected_chancellor(self.chancellor, self.board.fascist_board)
        if 4 <= self.board.fascist_board and self.chancellor.role is Role.HITLER:
            self.winner = BoardStates.HITLER_CHANCELLOR
            return True
        return False

    def enact_policy(self, remaining: Tuple[int, int]) -> Card:
        """ The elected government chooses which policy to enact.

        The deck is updated accordingly in this function.

        :param remaining: Tuple of how many liberal and fascist polices have not been seen
                by all of the players.
        :return The policy chosen:
        """
        policies = self.deck.draw_hand()
        p_pick = self.president.president_pick(self.chancellor.name, list(policies))
        shuffle(p_pick)
        c_pick = self.chancellor.chancellor_pick(self.president.name,
                                                 list(p_pick), remaining)
        Log.log_policy(policies, p_pick, c_pick)

        self.president.analyze_chancellor_card(self.chancellor.name, p_pick, c_pick)
        self.deck.discard(policies, [c_pick])
        return c_pick

    def vote(self) -> bool:
        """Votes to elect the current government.

        :return: If the the government was successfully elected.
        """
        ja = []
        nay = []
        for name, player in self.players.items():
            player_vote = player.vote(self.president.name, self.chancellor.name)
            if player_vote:
                ja.append(player.name)
            else:
                nay.append(player.name)
        Log.log_votes(self.president, self.chancellor, ja, nay)
        return len(ja) * 2 >= len(self.players)

    def analyze_revealed_card(self, next_policy: Card, remaining: Tuple[int, int]):
        """Has all of the players analyze the revealed card.

        :param next_policy: The policy that was enacted.
        :param remaining: The remaining cards.
        """
        for name, player in self.players.items():
            if name not in [self.chancellor.name, self.president_name]:
                player.analyze_revealed_card(self.president.name, self.chancellor.name,
                                             next_policy, remaining)

    def shoot(self, next_policy: Card)-> bool:
        """ Runs the shoot phase if apllicable.

        The phase runs if the enacted policy is the fourth or fifth fascist policy enacted
        and if the phase is enabled for this game.

        :param next_policy: The policy just enacted.
        :return: If Hitler was shot.
        """
        fascist_board = self.board.fascist_board
        if 4 <= fascist_board <= 5 and next_policy is Card.FASCIST and self.allow_shoots:
            player_shot = self.president.shoot(list(self.players.keys()))
            Log.log_shot_players(self.president, self.players[player_shot])
            if self.players[player_shot].role is Role.HITLER:
                self.winner = BoardStates.HITLER_SHOT
                return True
            self.remove_player(player_shot)
        return False

    def remove_player(self, player_shot: Name):
        """Removes a shot player from the game.

        :param player_shot: The player that was shot.
        """
        del self.players[player_shot]
        for name, player in self.players.items():
            player.remove_player(player_shot)

    @staticmethod
    def create_players(num_players: int) -> Dict[Name, Player]:
        """Creates the specified number of players and assigns them roles,
        the player strategies must be set later.

        :param: The number of players.
        :return: The dictionary of player names to player instances.
        """
        num_fascists = int((num_players - 1) / 2)
        fascists = []
        players = {}
        names = list(range(num_players))

        for i in names:
            players[i] = Player(i, names, num_fascists)

        names = list(names)
        shuffle(names)
        hitler = names.pop()
        chosen_fascists = 1

        while chosen_fascists < num_fascists:
            fascists.append(names.pop())
            chosen_fascists += 1
        for player in names:
            players[player].set_roles(Role.LIBERAL, {Role.FASCIST: [], Role.HITLER: None})
        for player in fascists:
            known_roles = {Role.FASCIST: list(fascists), Role.HITLER: hitler}
            players[player].set_roles(Role.FASCIST, known_roles)

        h_fascists = fascists if num_players < 6 else []
        known_roles = {Role.FASCIST: h_fascists, Role.HITLER: hitler}
        players[hitler].set_roles(Role.HITLER, known_roles)
        return players


__all__ = ["Game"]
