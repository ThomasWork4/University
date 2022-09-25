import math

def Calc_Weights(ti, ex):
    wi = (ti / ex) + ((1-ti) / (1-ex))
    return wi
