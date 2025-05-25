from typing import Optional, List, Dict, NamedTuple
from collections import Counter
import re
from dateutil.parser import parse
import datetime
import csv

class StockPrice(NamedTuple):
    symbol: str
    date: datetime.date
    closing_price: float

    def is_high_tech(self) -> bool:
        """It's a class, so we can add methods too"""
        return self.symbol in ['MSFT', 'GOOG', 'FB', 'AMZN', 'AAPL']

def try_parse_row(row: List[str]) -> Optional[StockPrice]:
    symbol, date_, closing_price_ = row

    # Stock symbol should be all capital letters
    if not re.match(r"^[A-Z]+$", symbol):
        return None

    try:
        date = parse(date_).date()
    except ValueError:
        return None

    try:
        closing_price = float(closing_price_)
    except ValueError:
        return None

    return StockPrice(symbol, date, closing_price)
with open("./aux_files/stocks.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = [[row['Symbol'], row['Date'], row['Close']]
            for row in reader]

# skip header
maybe_data = [try_parse_row(row) for row in rows]

# This is just to make mypy happy
data = [sp for sp in maybe_data if sp is not None]

# Imagine que queremos determinar o maior preço de fechamento da AAPL. Vamos fazer isso em etapas concretas:
# 1. Selecione apenas as linhas AAPL.
# 2. Selecione o closing_price de cada linha.
# 3. Calcule o max desses preços.

max_appl_price = max(stock_price.closing_price for stock_price in data if stock_price.symbol=="AAPL")
print(max_appl_price)

# De modo geral, queremos determinar o maior preço de fechamento de cada ação no conjunto de dados. Podemos fazer o seguinte:
# 1. Crie um dict para contrloar os preços mais altos (usaremos um defaultdict que retorna menos infinito para valores ausentes, pois
# todos os preços serão maiores que esse valor);
# 2. Itere nos dados, fazendo sua atualização.
from collections import defaultdict

max_prices: Dict[str, float] = defaultdict(lambda: float('-inf'))

for sp in data:
    symbol, closing_price = sp.symbol, sp.closing_price
    if closing_price > max_prices[symbol]:
        max_prices[symbol] = closing_price
        
        
# Agora vamos determinar as maiores e menores alterações percentuais registradas em um dia no conjunto de dados.
# Alteração percentual é price_today / price_yesterday - 1

# Agrupemos os preços por simbolos.
# Depois, em cada grupo:
# 1. Classifique os preços por data;
# 2. Use o zip para formar pares (anteriores, atuais);
# 3. Converta os pares em novas linhas de "alteração percentual";

# Gruping prices per symbo
# Colete os preços por simbolo
prices: Dict[str, List[StockPrice]] = defaultdict(list)

for sp in data:
    prices[sp.symbol].append(sp)

# Por serem tuplas os preços serão classificados da seguinte forma: campo: simbolo, data, preço, ordem.

# Classifique os preços por data
prices = {symbol: sorted(symbol_prices)
          for symbol, symbol_prices in prices.items()}

# Agora, calculamos uma sequência de alterações diárias;
def pct_change(yesterday: StockPrice, today: StockPrice) -> float:
    return today.closing_price / yesterday.closing_price -1


class DailyChange(NamedTuple):
    symbol: str
    date: datetime.date
    pct_change: float
    
def day_over_day_changes(prices: List[StockPrice]) -> List[DailyChange]:
    """
    Presume que os preços são de uma ação e estão classificados
    """
    return [DailyChange(symbol=today.symbol, date=today.date, pct_change=pct_change(yesterday, today))
            for yesterday, today in zip(prices, prices[1:])]

# Em seguida, coletamos todos:
all_changes = [change for symbol_prices in prices.values()
               for change in day_over_day_changes(symbol_prices)]



# In this step, is eazy to find the max and min value
max_change = max(all_changes, key=lambda change: change.pct_change)
print(max_change)
assert max_change.symbol == "AAPL"
assert max_change.date == datetime.date(1997, 8, 6)
assert 0.33 < max_change.pct_change < 0.34

min_change =min(all_changes, key=lambda change: change.pct_change)
print(min_change)
assert min_change.symbol == "AAPL"
assert min_change.date == datetime.date(2000, 9, 29)
assert -0.52 < min_change.pct_change < -0.51


# Agora utilizaremos destas informações para identificar o melhor mês para investir em ações de tecnologia. Analisaremos
# a alteração média diária de cada mês:
changes_by_month: List[DailyChange] = {month: [] for month in range(1,13)}

for change in all_changes:
    changes_by_month[change.date.month].append(change)
    
avg_daily_change = {
    month: sum(change.pct_change for change in changes) / len(changes)
    for month, changes in changes_by_month.items()
}

# Outubro é o melhor mês
print(max(avg_daily_change.values()))
assert avg_daily_change[10] == max(avg_daily_change.values())
