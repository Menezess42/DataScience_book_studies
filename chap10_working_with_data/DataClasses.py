# Dataclasses are (more or less) a mutable
# version of NamedTuple. (I say 'more or less'
# because NamedTuple represents your data compactly as
# tuples, but dataclasses are just regular Python classes
# that generate some methods automatically.)
# just python 3.7 and above

from dataclasses import dataclass
import datetime

@dataclass
class StockPrice2:
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self)-> float:
        '''
        Since it is a class, we can also add methods
        '''
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']

price2 = StockPrice2('MSFT', datetime.date(2018, 12, 14), 106.03)

assert price2.symbol == 'MSFT'
assert price2.closing_price == 106.03
assert price2.is_high_tech()

# The power of this one is that allows us to modify things
price2.closing_price /= 2
print(price2.closing_price)
