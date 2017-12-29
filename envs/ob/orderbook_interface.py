import numpy as np


class OrderBookInterface(object):
    """
    A blank orderbook that computes information
    about the orderbook with a variety of input
    sources: manual & automatic
    """

    def __init__(self):
        super(OrderBookInterface, self).__init__()
        self._bid = 0
        self._ask = float(9999999999)
        self._ask_vol = 0
        self._bid_vol = 0
        self._spread = 0
        self._imbalance = 0
        self._misbalance = 0
        self._smart_price = 0
        self._midquote = 0
        self._bid_limits = {}
        self._ask_limits = {}

    def refresh(self):
        self.bid = max(self._bid_limits.keys()) if len(
            self._bid_limits.keys()) > 0 else 0
        self.ask = min(self._ask_limits.keys()) if len(
            self._ask_limits.keys()) > 0 else float(9999999999)

        # safety check for when all orders at price level are cleared
        if self.bid in self._bid_limits:
            if self._bid_limits[self.bid].total_vol == 0:
                del self._bid_limits[self.bid]
                self.bid = 0

        # safety check for when all orders at price level are cleared
        if self.ask in self._ask_limits:
            if self._ask_limits[self.ask].total_vol == 0:
                del self._ask_limits[self.ask]
                self.ask = float(9999999999)

        self.bid_vol = self._bid_limits[self.bid].total_vol if len(
            self._bid_limits.keys()) > 0 else 0
        self.ask_vol = self._ask_limits[self.ask].total_vol if len(
            self._ask_limits.keys()) > 0 else 0

        self.spread = self.ask - self.bid
        self.midquote = (self.ask + self.bid) / 2.0
        self.imbalance = -np.log(self.bid_vol / self.ask_vol) if len(
            self._bid_limits.keys()) > 0 and len(
            self._ask_limits.keys()) > 0 else 0

        total_bid_vol = sum(list(map(
            lambda lvl: lvl.total_vol, self._bid_limits.values())))
        total_ask_vol = sum(list(map(
            lambda lvl: lvl.total_vol, self._ask_limits.values())))
        self.misbalance = -(total_ask_vol - total_bid_vol)

        smart_bid = self.bid * (1.0 / self.bid_vol) if len(
            self._bid_limits.keys()) > 0 else 0
        smart_ask = self.ask * (1.0 / self.ask_vol) if len(
            self._ask_limits.keys()) > 0 else 0
        self.smart_price = (smart_bid + smart_ask) / 2.0

    @property
    def bid(self):
        return self._bid

    @bid.setter
    def bid(self, val):
        if val > float(9999999999) or val < 0 or val is None:
            raise ValueError("Invalid bid")
        self._bid = float(val)

    @property
    def ask(self):
        return self._ask

    @ask.setter
    def ask(self, val):
        if val > float(9999999999) or val < 0 or val is None:
            raise ValueError("Invalid ask")
        self._ask = float(val)

    @property
    def bid_vol(self):
        return self._bid_vol

    @bid_vol.setter
    def bid_vol(self, val):
        if val < 0 or val is None:
            raise ValueError("Invalid volume")
        self._bid_vol = float(val)

    @property
    def ask_vol(self):
        return self._ask_vol

    @ask_vol.setter
    def ask_vol(self, val):
        if val < 0 or val is None:
            raise ValueError("Invalid volume")
        self._ask_vol = float(val)

    @property
    def imbalance(self):
        return self._imbalance

    @imbalance.setter
    def imbalance(self, val):
        if val is None:
            raise ValueError("Invalid imbalance")
        self._imbalance = float(val)

    @property
    def spread(self):
        return self._spread

    @spread.setter
    def spread(self, val):
        if val < 0:
            raise ValueError("Invalid volume")
        self._spread = float(val)

    @property
    def misbalance(self):
        return self._misbalance

    @misbalance.setter
    def misbalance(self, val):
        if val < 0 or val is None:
            raise ValueError("Invalid volume")
        self._misbalance = float(val)

    @property
    def smart_price(self):
        return self._smart_price

    @smart_price.setter
    def smart_price(self, val):
        if val < 0 or val is None:
            raise ValueError("Invalid volume")
        self._smart_price = float(val)

    @property
    def midquote(self):
        return self._midquote

    @midquote.setter
    def midquote(self, val):
        if val < 0 or val is None:
            raise ValueError("Invalid volume")
        self._midquote = float(val)