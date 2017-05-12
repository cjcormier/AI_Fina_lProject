from random import shuffle
from secret_hitler_ai.deck import *
from secret_hitler_ai.player import *
from secret_hitler_ai.board import *
from secret_hitler_ai.roles import Role
from secret_hitler_ai.logging import Log
from secret_hitler_ai.cards import Cards


class Game:
    def __init__(self, num_players, allow_shoots=False, log=None):
        self.num_players = num_players
        self.players = self.assign_roles()
        self.orig_players = dict(self.players)
        self.allow_shoots = allow_shoots
        self.board = Board()
        self.deck = Deck(6, 11)
        self.winner = BoardStates.NORMAL
        self.log = log if type(log) is Log else Log()

        self.prev_pres = -1
        self.president_name = -1
        self.president = None
        self.chancellor = None
        self.anarchies = 0

    def run(self):
        rounds = 0
        Log.log('ROLES')
        for player in self.players.values():
            Log.log('{}: {}'.format(player.name, player.role))
        while self.winner is BoardStates.NORMAL:
            rounds += 1
            Log.log_new_round()
            self.round()
        self.log.log_game_results(rounds)

        return self.winner, self. board.fascist_board, self.board.liberal_board, self.anarchies

    def round(self):
        if self.elect_new_gov():
            self.log.record_gov(self.president, self.chancellor)
            self.prev_pres = self.president_name
            if self.check_hitler_chanc_win():
                return
            next_policy = self.choose_policy()
            self.analyze_revealed_card(next_policy)
        else:
            next_policy = self.deck.draw()
            self.anarchies += 1
            Log.log_anarchy()
        self.winner = self.board.increment_board(next_policy)
        Log.log_next_policy(next_policy)
        self.shoot(next_policy)
        Log.log_all_probs(self.players, self.orig_players)

    def elect_new_gov(self):
        rounds_of_voting = 0
        vote_passed = False
        while not vote_passed and rounds_of_voting < 3:  # until the vote passes or 3 votes fail
            rounds_of_voting += 1
            self.next_pres()
            self.president, self.chancellor = self.propose_gov()

            vote_passed = self.vote()
            Log.log_vote_results(vote_passed, rounds_of_voting)
        return vote_passed

    def next_pres(self):
        # TODO actually get next pres from list
        self.president_name = (self.president_name + 1) % self.num_players
        while self.president_name not in self.players.keys():
            self.president_name = (self.president_name + 1) % self.num_players

    def propose_gov(self):
        players = self.players.keys()
        chancellor_name = self.chancellor.name if self.chancellor is not None else -1

        names = [x for x in players if x is not chancellor_name and x is not self.president_name]
        names = [x for x in names if x is not self.prev_pres] if len(self.players) > 5 else names
        Log.log_valid_chancellors(names)

        president = self.players[self.president_name]
        chancellor_name = president.choose_chancellor(names)
        chancellor = self.players[chancellor_name]
        assert president is not chancellor
        return president, chancellor

    def check_hitler_chanc_win(self):
        Log.log_elected_chancellor(self.chancellor, self.board.fascist_board)
        if 4 <= self.board.fascist_board and self.chancellor.role is Role.HITLER:
            self.winner = BoardStates.HITLER_CHANCELLOR
            return True
        return False

    def choose_policy(self):
        remaining = self.deck.total_remaining()
        policies = self.deck.draw_hand()
        p_pick = self.president.president_pick(self.chancellor.name, list(policies))
        c_pick = self.chancellor.chancellor_pick(self.president.name, list(p_pick), remaining)
        Log.log_policy(policies, p_pick, c_pick)

        self.president.analyze_chancellor_card(self.chancellor.name, p_pick, c_pick)
        self.deck.discard(policies, c_pick)
        return c_pick

    def vote(self):
        ja = []
        nay = []
        for name, player in self.players.items():
            player_vote = player.vote(self.president.name, self.chancellor.name)
            if player_vote:
                ja.append(player.name)
            else:
                nay.append(player.name)
        Log.log_votes(self.president, self.chancellor, ja, nay)
        return len(ja)*2 >= len(self.players)

    def analyze_revealed_card(self, next_policy):
        for name, player in self.players.items():
            if name not in [self.chancellor.name, self.president_name]:
                player.analyze_revealed_card(self.president.name, self.chancellor.name,
                                             next_policy, self.deck.total_remaining())

    def shoot(self, next_policy):
        fascist_board = self.board.fascist_board
        if 4 <= fascist_board <= 5 and next_policy is Cards.FASCIST and self.allow_shoots:
            player_shot = self.president.shoot(list(self.players.keys()))
            Log.log_shot_players(self.president, self.players[player_shot])
            if self.players[player_shot].role is Role.HITLER:
                self.winner = BoardStates.HITLER_SHOT
                return False
            self.remove_player(player_shot)
        return True

    def remove_player(self, player_shot):
        del self.players[player_shot]
        for name, player in self.players.items():
            player.remove_player(player_shot)

    def assign_roles(self):
        num_fascists = int((self.num_players-1)/2)
        fascists = []
        players = {}
        names = list(range(self.num_players))

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
            players[player].set_role(Role.LIBERAL, {Role.FASCIST: [], Role.HITLER: None})
        for player in fascists:
            players[player].set_role(Role.FASCIST, {Role.FASCIST: list(fascists), Role.HITLER: hitler})

        h_fascists = fascists if self.num_players < 6 else []
        players[hitler].set_role(Role.HITLER, {Role.FASCIST: h_fascists, Role.HITLER: hitler})
        return players

__all__ = ["Game"]
