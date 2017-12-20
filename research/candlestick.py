class CandleStick:
    open = high = low = close = 0

    def __init__(self, open, high, low, close):
        self.open = open
        self.high = high
        self.low = low
        self.close = close

    def is_red(self):
        if self.close < self.open:
            return True
        else:
            return False

    def is_green(self):
        if self.close > self.open:
            return True
        else:
            return False
