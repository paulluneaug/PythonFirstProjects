from random import random

def randprob(prob):
    """
    Renvoie True selon une certaine probabilité "prob"

    Arguments:
    ¯¯¯¯¯¯¯¯¯
        prob: type = float or int ; 0 <= prob <= 1
            Probabilité de retourner True

    Return:
    ¯¯¯¯¯¯
        tf: type = bool
            True ou False selon la probabilité "prob" et un tirage aléatoire
    """
    return random()<=prob


print([randprob(0) for i in range(1236265216232126516221062522)].count(True))