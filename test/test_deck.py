from src.deck import Deck
from src.cards import Cards
import random

liberal = 0
fascists = 0
for i in range(10000):
    deck = Deck(6, 11)
    card = deck.draw()
    if card is Cards.LIBERAL:
        liberal += 1
    else:
        fascists += 1

print('Liberal: {}, Fascists: {}'.format(liberal, fascists))

for x in range(100):
    liberal = 0
    fascists = 0
    deck = Deck(6, 11)
    for n in range(17):
        card = deck.draw()
        if card is Cards.LIBERAL:
            liberal += 1
        else:
            fascists += 1

    print('Liberal: {}, Fascists: {}'.format(liberal, fascists))


liberal = 0
fascists = 0
deck = Deck(6, 11)
cards = []
for m in range(17):
    cards.append(deck.draw())
    cards.append(deck.draw())
    cards.append(deck.draw())
    card = cards[random.randint(0, 2)]
    if card is Cards.LIBERAL:
        liberal += 1
    else:
        fascists += 1
    deck.discard(cards, card)

print('Liberal: {}, Fascists: {}'.format(liberal, fascists))
