import csv
from datetime import datetime

def log_trade(symbol, side, entry, exit_price, amount, profit, reason):
    with open("data/profits.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.utcnow(), symbol, side, entry, exit_price, amount, profit, reason])
