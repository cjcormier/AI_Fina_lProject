"""
Helper functions for various strategies.
"""
from secret_hitler_ai.player import  Player


def multi_3(num: int):
    """
    num!/(num - 3)!
    """
    return num*(num-1)*(num-2)


def multi_2(num: int):
    """
    num!/(num - 2)!
    """
    return num*(num-1)

def pass_strat(*args):
    """
    Strategy to do nothing.
    """
    pass


# TODO: Explain analysis better.
def baysian_markov_analysis(inv_model: float, recursive_term: float,
                            prior_term: float)->float:
    """
    Performs the baysian markov analysis.
    
    :param inv_model: Probablilty based on current observations.
    :param recursive_term: Previous probability based on all previous observation
    :param prior_term: The original probability
    :return: The new probability based on all observations
    """
    # if inv_model == 1 or recursive_term == 1:
    #     return 0.0

    gama_result = product_gama(inv_model, recursive_term, prior_term)
    return 1/(1+gama_result)


def product_gama(inv_model: float, recursive_term: float, prior: float)->float:
    """
    Return the product of the gama terms.
    
    :param inv_model: Probablilty based on current observations.
    :param recursive_term: Previous probability based on all previous observation
    :param prior: The original probability
    :return: 
    """
    return inverse_gama(inv_model) * inverse_gama(recursive_term) * gama(prior)


def gama(x: float)->float:
    """
    Return the gama term.
    
    :param x: The term to get the gama term of.
    :return:  The gama term.
    """
    return float('Inf') if x == 1 else x/(1-x)


def inverse_gama(x: float) -> float:
    """
    Return the inverse gama term.

    :param x: The term to get the inverse gama term of.
    :return:  The inverse gama term.
    """
    return float('Inf') if x == 0 else (1-x)/x