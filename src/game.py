from random import shuffle
from src.deck import *
from src.player import *
from src.board import *


def game(num_players):
    board = Board()
    deck = Deck(11, 6)

    winner = None
    players = assign_roles(num_players)

    pres = 0
    president = None
    chancellor = None

    while winner is not BoardStates.FASCIST_WIN and winner is not BoardStates.LIBERAL_WIL:              # until someone wins loop this
        vote_passed = False
        i = 0
        while not vote_passed and i < 3:  # until the vote passes or 3 votes fail
            i += 1

            pres = pres+1 if pres < num_players else 0
            president, chancellor = new_gov(players, pres)
            vote_passed = vote(players, president, chancellor)

        if vote_passed:              # if loop terminated in a yay vote
            if 4 <= board.fascist_board <= 5 and chancellor.role is Role.HITLER:
                winner = 'BoardStates.FASCIST_WIN'
            next_policy = chancellor.chancellor_pick(president.president_pick(deck.draw_hand()))
        else:                       # if loop terminated due to 3 nay votes
            next_policy = deck.draw()

        winner = board.increment_board(next_policy)
    return


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

    for player in fascists:
        players[player].set_role(Role.FASCIST, {Role.FASCIST: fascists, Role.HITLER: hitler})

    if num_players > 6:
        fascists = None
    players[hitler].set_role(Role.HITLER, {Role.FASCIST: fascists})

    return players


def new_gov(players, pres):
    president = players[pres]
    chanc = president.choose_chancellor(players)  # limit valid players
    chancellor = players[chanc]
    return president, chancellor


def vote(players, president, chancellor):
    votes = 0
    for player in players:
        if player.vote(president, chancellor):
            votes += 1
    return votes > (activePlayers / 2)
