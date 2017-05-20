"""
Strategies to analyze the revealed chancellor card.
"""
from secret_hitler_ai.deck import Card
from secret_hitler_ai.logging import Log
from secret_hitler_ai.player import Player, Name
from typing import List


def analyze_chancellor_card(player: Player, chancellor: Name,
                            pres_cards: List[Card], chanc_card: Card):
    """
    Analyzes the card the chancellor chose to enact given the choices that the chancellor 
    was given.
    
    :param player: The player analyzing the revealed card, (usually the president).
    :param chancellor: The chancellor who 
    :param pres_cards: 
    :param chanc_card: 
    :return: 
    """
    if chanc_card == Card.FASCIST and Card.LIBERAL in pres_cards:
        message = "Player {} thinks chancellor {} is a Fascist because they were given" \
                  " a choice and played a fascist policy."
        Log.log(message, (player.name, chancellor))
        if chancellor not in player.fascists:
            player.fascists.append(chancellor)

        player.set_prob(chancellor, 1)


__all__ = ["analyze_chancellor_card"]
