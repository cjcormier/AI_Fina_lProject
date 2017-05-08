from random import randint
from src.cards import Cards
from src.logging import Log


class Deck:
    def __init__(self, liberal, fascist):
        self.libDeck = liberal
        self.facDeck = fascist
        self.facDisc = 0
        self.libDisc = 0

    def draw(self):
        if self.libDeck + self.facDeck <= 2:
            self.libDeck += self.libDisc
            self.facDeck += self.facDisc
            self.libDisc = 0
            self.facDisc = 0

        card = randint(0, self.libDeck + self.facDeck - 1)
        if card < self.libDeck:
            self.libDeck -= 1
            card = Cards.LIBERAL
        else:
            self.facDeck -= 1
            card = Cards.FASCIST
        return card

    def draw_hand(self):
        c1 = self.draw()
        c2 = self.draw()
        c3 = self.draw()
        return [c1, c2, c3]

    def discard(self, drawn_cards, played_cards):
        drawn_cards.remove(played_cards)
        for card in drawn_cards:
            if card is Cards.LIBERAL:
                self.libDisc += 1
            else:
                self.facDisc += 1

    def total_remaining(self):
        return self.libDeck+self.libDisc, self.facDeck+self.facDisc

__all__ = ['Deck']
