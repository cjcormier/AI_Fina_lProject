from src.strategies import *
from src.logging import Log

de_prob_val = .3
curr_prob = 0
message = 'Factor {}, Default Prob: {}, Curr Prob: {}, Adjust: {}'

for factor in range(-10, 31, 1):
    set_adjust_factor(factor/10)
    for i in range(0, 11, 1):
        curr_prob = i/10
        Log.log(message.format(factor/10, de_prob_val, curr_prob, adjust(curr_prob, de_prob_val)))
