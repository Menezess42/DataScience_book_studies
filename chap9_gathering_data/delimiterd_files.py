# > Never analise a comma-separated file on your own.
# > You will mess up the edge cases.

# If the file has no header (indicating that each
#  line has to be a list and that you have to know
#  the content of each column), use the csv.reader
# to iterate on each line in a way that each one
# generates a separated list in the correct maner.

# Example, imagine that we have a file delimited by
# tabs with stock prices.
'''
6/20/2014   AAPL    90.91
6/20/2014   MSFT    41.68
6/20/2014   FB    41.68
6/19/2014   AAPL    91.86
6/19/2014   MSFT    41.51
6/19/2014   FB    64.34
'''
def process(date: str, symbol: str, closing_price: float) -> None:
    # Imaginge that this function actually does something.
    assert closing_price > 0.0
    print(date)
    print(symbol)
    print(closing_price)

# We can process in this way:
import csv
with open('tab_delimited_stock_prices.txt', 'w') as f:
    f.write("""6/20/2014\tAAPL\t90.91
6/20/2014\tMSFT\t41.68
6/20/2014\tFB\t64.5
6/19/2014\tAAPL\t91.86
6/19/2014\tMSFT\t41.51
6/19/2014\tFB\t64.34
""")

with open('tab_delimited_stock_prices.txt') as f:
    tab_reader = csv.reader(f, delimiter='\t')
    for i, row in enumerate(tab_reader):
        date = row[0]
        symbol = row[1]
        closing_price = float(row[2])
        process(date, symbol, closing_price)

# If the file has header:
'''
date:symbol:closing_rice
6/20/2014:MSFT:41.68
6/20/2014:FB:64.5
6/19/2014:AAPL:91.86
6/19/2014:MSFT:41.51
6/19/2014:FB:64.34
'''
with open('colon_delimited_stock_prices.txt', 'w') as f:
    f.write("""date:symbol:closing_price
6/20/2014:AAPL:90.91
6/20/2014:MSFT:41.68
6/20/2014:FB:64.5
""")
# It's possible ignor the header line with a initial call
# to reader.next or recive each line as a dict (using the header
# as keys) with csv.DictReader:
with open('colon_delimited_stock_prices.txt') as f:
    colon_reader = csv.DictReader(f, delimiter=':')
    for dict_row in colon_reader:
        date = dict_row['date']
        symbol = dict_row['symbol']
        closing_price = float(dict_row['closing_price'])
        process(date, symbol, closing_price)

# Even if the files has no header, you can use the DictReader
# passing the keys as fieldnames parameters.

# In the same way, it's possible write the delimited data using
# csv.writer:
todays_price = {'AAPL': 90.91, 'MSFT': 41.68, 'FB': 64.5}

with open('comma_delimited_stock_prices.txt', 'w') as f:
    csv_writer = csv.writer(f, delimiter=',') 
    for stock, price in todays_price.items():
        csv_writer.writerow([stock, price])
