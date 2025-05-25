# Alternative to dicts
from collections import namedtuple
import datetime
stockPrice = namedtuple('stockPrice', ['symbol', 'date', 'closing_price'])
price = stockPrice('MSFT', datetime.date(2018, 12, 14), 106.03)

# Type notation
from typing import NamedTuple

class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float
    
    def is_high_tech(self) -> bool:
        '''
        It's a class so we can add methods
        '''
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZ', 'AAPL']

