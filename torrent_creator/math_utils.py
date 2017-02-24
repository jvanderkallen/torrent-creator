import math

def is_power(value, power):
    exponent = math.log(value) / math.log(power)
    return int(exponent) == exponent
