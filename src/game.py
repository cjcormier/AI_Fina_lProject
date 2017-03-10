from random import shuffle
from src.deck import *
from src.player import *
from src.board import *
from src.roles import Role
from src.logging import Log
from src.cards import Cards


class Game:
    def __init__(self, num_players, allow_shoots=False):
        self.num_players = num_players
        self.players = self.assign_roles()
        self.allow_shoots = allow_shoots
        self.board = Board()
        self.deck = Deck(6, 11)
        self.winner = BoardStates.NORMAL

        self.prev_pres = -1
        self.president_name = -1
        self.president = None
        self.chancellor = None

        self.anarchies = 0
        self.l_pres = 0
        self.f_pres = 0
        self.h_pres = 0
        self.l_chanc = 0
        self.f_chanc = 0
        self.h_chanc = 0

    def run(self):
        rounds = 0
        while self.winner is BoardStates.NORMAL:
            rounds += 1
            self.round()
        message = '\n{} rounds:\n{} liberal presidents, {} fascist presidents and {} hitler ' \
                  'presidents\n{} liberal chancellors, {} fascist chancellors and {} hitler ' \
                  'chancellors.'
        Log.log(message.format(rounds, self.l_pres, self.f_pres, self.h_pres, self.l_chanc,
                               self.f_chanc, self.h_chanc))

        return self.winner, self. board.fascist_board, self.board.liberal_board, self.anarchies

    def round(self):
        Log.log('\n------------------------\n\nNew Round')

        if self.elect_new_gov():
            self.record_gov()
            self.prev_pres = self.president_name
            Log.log("Vote Passed")
            if self.check_hitler_chanc_win():
                return
            next_policy = self.choose_policy()
            self.analyze_revealed_card(next_policy)
        else:
            next_policy = self.deck.draw()
            self.anarchies += 1
            Log.log('Anarchy!!!!!')
        self.winner = self.board.increment_board(next_policy)
        Log.log('Next Policy:', next_policy)
        self.shoot(next_policy)

    def elect_new_gov(self):
        rounds_of_voting = 0
        vote_passed = False
        while not vote_passed and rounds_of_voting < 3:  # until the vote passes or 3 votes fail
            rounds_of_voting += 1
            self.next_pres()
            self.president, self.chancellor = self.propose_gov()

            message = "Voting on new government. President: {} Chancellor: {} ({},{})"
            Log.log(message.format(self.president_name, self.chancellor.name, self.president.role,
                                   self.chancellor.role))
            vote_passed = self.vote()
            if not vote_passed:
                Log.log('Vote Failed, number of consecutive failed votes:', rounds_of_voting)
        return vote_passed

    def next_pres(self):
        # TODO actually get next pres from list
        self.president_name = (self.president_name + 1) % self.num_players
        while self.president_name not in self.players.keys():
            self.president_name = (self.president_name + 1) % self.num_players

    def propose_gov(self):
        players = self.players.keys()
        chancellor_name = self.chancellor.name if self.chancellor is not None else -1
        names = [x for x in players if x is not chancellor_name]
        names = [x for x in names if x is not self.prev_pres] if len(self.players) > 5 else names
        Log.log('Valid chancellors: {}'.format(names))

        president = self.players[self.president_name]
        chancellor_name = president.choose_chancellor(names)  # limit valid players
        chancellor = self.players[chancellor_name]
        return president, chancellor

    def check_hitler_chanc_win(self):
        if 4 <= self.board.fascist_board <= 5 and self.chancellor.role is Role.HITLER:
            Log.log('Chancellor {} is Hitler, fascists win!'.format(self.chancellor.name))
            self.winner = BoardStates.HITLER_CHANCELLOR
            return True
        return False

    def choose_policy(self):
        remaining = self.deck.total_remaining()
        policies = self.deck.draw_hand()
        p_pick = self.president.president_pick(self.chancellor.name, list(policies))
        c_pick = self.chancellor.chancellor_pick(self.president.name, list(p_pick), remaining)
        message = '\nDrawn Cards:{}\nPres Pick: {}, Canc Pick: {}\n'
        Log.log(message.format(policies, p_pick, c_pick))

        self.president.analyze_chancellor_card(self.chancellor.name, p_pick, c_pick)
        self.deck.discard(policies, c_pick)
        return c_pick

    def vote(self):
        votes = 0
        ja = []
        nay = []
        for name, player in self.players.items():
            player_vote = player.vote(self.president.name, self.chancellor.name)
            if player_vote:
                votes += 1
                ja.append(player.name)
            else:
                nay.append(player.name)
        message = 'Votes in favor: {}, Votes against: {}  ({},{})'
        Log.log(message.format(ja, nay, votes, len(self.players) - votes))
        return votes >= (len(self.players) / 2)

    def record_gov(self):
        if self.president.role is Role.LIBERAL:
            self.l_pres += 1
        elif self.president.role is Role.FASCIST:
            self.f_pres += 1
        elif self.president.role is Role.HITLER:
            self.h_pres += 1

        if self.chancellor.role is Role.LIBERAL:
            self.l_chanc += 1
        elif self.chancellor.role is Role.FASCIST:
            self.f_chanc += 1
        elif self.chancellor.role is Role.HITLER:
            self.h_chanc += 1

    def analyze_revealed_card(self, next_policy):
        for name, player in self.players.items():
            player.analyze_revealed_card(self.president.name, self.chancellor.name,
                                         next_policy, self.deck.total_remaining())

    def shoot(self, next_policy):
        fascist_board = self.board.fascist_board
        if 4 <= fascist_board <= 5 and next_policy is Cards.FASCIST and self.allow_shoots:
            player_shot = self.president.shoot()
            Log.log('President {} shot player {}.'.format(self.president.name, player_shot))
            if self.players[player_shot].role is Role.HITLER:
                Log.log('Player {} is Hitler, liberals win!'.format(player_shot))
                self.winner = BoardStates.HITLER_SHOT
                return False
            else:
                message = 'Player {0} is not Hitler. ({0} was {1} instead and {2} was {3}.)'
                Log.log(message.format(player_shot, self.players[player_shot].role,
                                       self.president.name, self.president.role))
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
            players[player].set_role(Role.FASCIST, {Role.FASCIST: fascists, Role.HITLER: hitler})

        h_fascists = fascists if self.num_players < 6 else []
        players[hitler].set_role(Role.HITLER, {Role.FASCIST: h_fascists, Role.HITLER: hitler})
        return players

__all__ = [Game]
