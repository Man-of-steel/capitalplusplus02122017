def is_bullish_engulfing(c1, c2):
    if c1.is_red() and c2.is_green() and c2.low < c1.low and c2.high > c1.high:
        return True
    else:
        return False


def is_uptrend(c1, c2):
    if c1.is_green() and c2.is_green() and c2.high > c1.high and c2.low > c1.low:
        return True
    else:
        return False



