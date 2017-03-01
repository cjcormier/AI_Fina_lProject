from random import shuffle
from src.deck import *
from src.player import *
from src.board import *
from src.roles import Role
from src.logging import Log


def game(num_players, players, allow_shoots=False):
    board = Board()
    deck = Deck(6, 11)
    winner = BoardStates.NORMAL

    prev_pres = -1
    president_name = -1
    president = None
    chancellor = None
    anarchies = 0
    l_pres = 0
    f_pres = 0
    h_pres = 0
    l_chanc = 0
    f_chanc = 0
    h_chanc = 0
    rounds = 0

    print_roles(players)

    # until someone wins loop this
    while winner is BoardStates.NORMAL:
        rounds += 1
        Log.log('\n------------------------\n\nNew Round')
        vote_passed = False
        rounds_of_voting = 0
        while not vote_passed and rounds_of_voting < 3:  # until the vote passes or 3 votes fail
            rounds_of_voting += 1
            president_name = (president_name+1) % num_players
            while president_name not in players.keys():
                president_name = (president_name+1) % num_players

            president, chancellor = new_gov(players, president_name, prev_pres, chancellor)

            message = "Voting on new government. President: {} Chancellor: {} ({},{})"
            Log.log(message.format(president_name, chancellor.name, president.role,
                                   chancellor.role))
            vote_passed = vote(players, president, chancellor)
            if not vote_passed:
                Log.log('Vote Failed, number of consecutive failed votes:', rounds_of_voting)

        if vote_passed:              # if loop terminated in a yay vote
            l_pres, f_pres, h_pres, l_chanc, f_chanc, h_chanc = \
                record_gov(l_pres, f_pres, h_pres, l_chanc,
                           f_chanc, h_chanc, president, chancellor)
            prev_pres = president_name
            Log.log("Vote Passed")
            if 4 <= board.fascist_board <= 5 and chancellor.role is Role.HITLER:
                Log.log('Chancellor {} is Hitler, fascists win!'.format(chancellor.name))
                winner = BoardStates.HITLER_CHANCELLOR
                continue

            next_policy = choose_policy(president, chancellor, deck)

            for name, player in players.items():
                player.analyze_revealed_card(president.name, chancellor.name,
                                             next_policy, deck.total_remaining())

            if 4 <= board.fascist_board <= 5 and next_policy is Cards.FASCIST and allow_shoots:
                winner = shoot(president, players)
                if winner is not BoardStates.NORMAL:
                    continue

        else:                       # if loop terminated due to 3 nay votes
            next_policy = deck.draw()
            anarchies += 1
            Log.log('Anarchy!!!!!')

        Log.log('Next Policy:', next_policy)
        winner = board.increment_board(next_policy)
    message = '\n{} rounds:\n{} liberal presidents, {} fascist presidents and {} hitler ' \
              'presidents\n{} liberal chancellors, {} fascist chancellors and {} hitler ' \
              'chancellors.'
    Log.log(message.format(rounds, l_pres, f_pres, h_pres, l_chanc, f_chanc, h_chanc))
    return winner, board.fascist_board, board.liberal_board, anarchies


def assign_roles(num_players):
    num_fascists = int((num_players-1)/2)
    fascists = []
    players = {}
    names = list(range(num_players))

    for i in names:
        players[i] = Player(i, names, num_fascists)

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


def shoot(president, players):
    player_shot = president.shoot()
    Log.log('President {} shot player {}.'.format(president.name, player_shot))
    if players[player_shot].role is Role.HITLER:
        Log.log('Player {} is Hitler, liberals win!'.format(player_shot))
        return BoardStates.HITLER_SHOT
    else:
        message = 'Player {0} is not Hitler. ({0} was {1} instead and {2} was {3}.)'
        Log.log(message.format(player_shot, players[player_shot].role,
                               president.name, president.role))
    del players[player_shot]
    for name, player in players.items():
        player.remove_player(player_shot)
    return BoardStates.NORMAL


def print_roles(players):
    for name, player in players.items():
        Log.log("Player {} is {}".format(player.name, player.role))
        # player.print_probs()


def choose_policy(president, chancellor, deck):
    remaining = deck.total_remaining()
    policies = deck.draw_hand()

    president_pick = president.president_pick(chancellor.name, list(policies))
    chancellor_pick = chancellor.chancellor_pick(president.name, list(president_pick), remaining)

    Log.log('\nDrawn Cards:{}\nPres Pick: {}, Canc Pick: {}\n'.format(policies, president_pick,
                                                                      chancellor_pick))

    president.analyze_chancellor_card(chancellor.name, president_pick, chancellor_pick)
    deck.discard(policies, chancellor_pick)
    return chancellor_pick


def new_gov(players, pres, prev_pres, chancellor):
    chancellor_name = chancellor.name if chancellor is not None else -1
    names = [x for x in players.keys() if x is not prev_pres and x is not chancellor_name]
    Log.log('Valid chancellors: {}'.format(names))
    president = players[pres]
    chancellor_name = president.choose_chancellor(names)  # limit valid players
    chancellor = players[chancellor_name]
    return president, chancellor


def vote(players, president, chancellor):
    votes = 0
    ja = []
    nay = []
    for name, player in players.items():
        player_vote = player.vote(president.name, chancellor.name)
        if player_vote:
            votes += 1
            ja.append(player.name)
        else:
            nay.append(player.name)

    Log.log('Votes in favor: {}, Votes against: {}  ({},{})'.format(ja, nay, votes,
                                                                    len(players)-votes))
    return votes >= (len(players) / 2)


def record_gov(l_pres, f_pres, h_pres, l_chanc, f_chanc, h_chanc, president, chancellor):
    if president.role is Role.LIBERAL:
        l_pres += 1
    elif president.role is Role.FASCIST:
        f_pres += 1
    elif president.role is Role.HITLER:
        h_pres += 1

    if chancellor.role is Role.LIBERAL:
        l_chanc += 1
    elif chancellor.role is Role.FASCIST:
        f_chanc += 1
    elif chancellor.role is Role.HITLER:
        h_chanc += 1

    return l_pres, f_pres, h_pres, l_chanc, f_chanc, h_chanc
