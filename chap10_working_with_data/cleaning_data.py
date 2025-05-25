from dateutil.parser import parse
from using_NamedTuples import StockPrice
from typing import List
import datetime


# It is possible to reduce the error-proneness if the
# analysis is done in a testable function.
def parse_row(row: List[str]) -> StockPrice:
    symbol, date, closing_price = row
    return StockPrice(symbol=symbol,
                      date=parse(date).date(),
                      closing_price=float(closing_price))


# Now we test
stock = parse_row(['MSFT', '2018-12-14', '106.03'])

# assert stock.symbol == 'MSFT'
# assert stock.date == datetime.date(2018, 12, 14)
# ssert stock.closing_price == 106.03

from typing import Optional
import re
def try_parse_row(row: List[str])-> Optional[StockPrice]:
    symbol, date_, closing_price_ = row
    # The symbols of the stocks has to be CAPSLOCK
    if not re.match(r"^[A-Z]+$", symbol):
        return None

    try:
        date= parse(date_).date()
    except ValueError:
        return None

    try: cllosing_price = float(closing_price_)
    except ValueError: return None


# Must return None in wrong cases
# assert try_parse_row(['MSFT0', '2018-12-14', '106.03']) is None
# assert try_parse_row(['MSFT', '2018-12--14', '106.03']) is None
# assert try_parse_row(['MSFT', '2018-12-14', 'x']) is None

# Valid data


# Exemple
import csv

data: List[StockPrice] = []

with open('./aux_files/comma_delimited_stock_prices.txt') as f:
    readers = csv.reader(f)
    print(readers)
    for fs,x in enumerate(readers):
        print(fs)
        print(x)
    for row in readers:
        print(row)
        maybe_stock = try_parse_row(row)
        if maybe_stock is None:
            print(f"Skipping invalid row: {row}")
        else:
            data.append(maybe_stock)


