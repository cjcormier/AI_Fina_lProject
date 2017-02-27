from random import shuffle
from src.deck import *
from src.player import *
from src.board import *


def game(num_players, players=None):
    board = Board()
    deck = Deck(6, 11)
    winner = None

    prev_pres = -1
    president_name = -1
    president = None
    chancellor = None
    anarchies = 0

    print_roles(players)

    # until someone wins loop this
    while winner is not BoardStates.FASCIST_WIN and winner is not BoardStates.LIBERAL_WIN:
        print('\n------------------------\n\nNew Round')
        vote_passed = False
        rounds_of_voting = 0
        while not vote_passed and rounds_of_voting < 3:  # until the vote passes or 3 votes fail
            rounds_of_voting += 1
            president_name = (president_name+1) % num_players
            president, chancellor = new_gov(players, president_name, prev_pres, chancellor)

            message = "Voting on new government. President: {} Chancellor: {} ({},{})"
            print(message.format(president_name, chancellor.name, president.role, chancellor.role))
            vote_passed = vote(players, president, chancellor)
            if not vote_passed:
                print('Vote Failed, number of consecutive failed votes:', rounds_of_voting)

        if vote_passed:              # if loop terminated in a yay vote
            prev_pres = president_name
            print("Vote Passed")
            if 4 <= board.fascist_board <= 5 and chancellor.role is Role.HITLER:
                print('Chancellor {} is Hitler, fascists win!'.format(chancellor.name))
                winner = BoardStates.FASCIST_WIN
            next_policy = choose_policy(president, chancellor, deck)
            for player in players:
                player.analyze_revealed_card(president.name, chancellor.name,
                                             next_policy, deck.total_remaining())
        else:                       # if loop terminated due to 3 nay votes
            next_policy = deck.draw()
            anarchies += 1
            print('Anarchy!!!!!')

        print('Next Policy:', next_policy)
        winner = board.increment_board(next_policy)
    return winner, board.fascist_board, board.liberal_board, anarchies


def assign_roles(num_players):
    num_fascists = int((num_players-1)/2)
    fascists = []
    players = []
    names = list(range(num_players))

    for i in names:
        players.append(Player(i, names, num_fascists))

    names = list(names)
    shuffle(names)

    chosen_fascists = 0
    hitler = names.pop()
    chosen_fascists += 1

    while chosen_fascists < num_fascists:
        fascists.append(names.pop())
        chosen_fascists += 1

    for player in names:
        players[player].set_role(Role.LIBERAL, {Role.FASCIST: [], Role.HITLER: None})

    for player in fascists:
        players[player].set_role(Role.FASCIST, {Role.FASCIST: fascists, Role.HITLER: hitler})

    if num_players > 6:
        fascists = []
    players[hitler].set_role(Role.HITLER, {Role.FASCIST: fascists, Role.HITLER: hitler})

    return players


def print_roles(players):
    for player in players:
        print("Player {} is {}".format(player.name, player.role))
        # player.print_probs()


def choose_policy(president, chancellor, deck):
    remaining = deck.total_remaining()
    policies = deck.draw_hand()

    president_pick = president.president_pick(chancellor.name, list(policies))
    chancellor_pick = chancellor.chancellor_pick(president.name, list(president_pick), remaining)

    print('\nDrawn Cards:{}\nPres Pick: {}, Canc Pick: {}\n'.format(policies, president_pick,
                                                                    chancellor_pick))

    president.analyze_chancellor_card(chancellor.name, president_pick, chancellor_pick)
    deck.discard(policies, chancellor_pick)
    return chancellor_pick


def new_gov(players, pres, prev_pres, chancellor):
    chancellor_name = chancellor.name if chancellor is not None else -1
    names = [x.name for x in players if x.name is not prev_pres and x.name is not chancellor_name]
    print('Valid chancellors: {}'.format(names))
    president = players[pres]
    chancellor_name = president.choose_chancellor(names)  # limit valid players
    chancellor = players[chancellor_name]
    return president, chancellor


def vote(players, president, chancellor):
    votes = 0
    ja = []
    nay = []
    for player in players:
        player_vote = player.vote(president.name, chancellor.name)
        if player_vote:
            votes += 1
            ja.append(player.name)
        else:
            nay.append(player.name)

    print('Votes in favor: {}, Votes against: {}  ({},{})'.format(ja, nay, votes,
                                                                  len(players)-votes))
    return votes >= (len(players) / 2)
