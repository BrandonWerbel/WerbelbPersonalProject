import requests
import time
import json

class Simulator:

    def __init__(self, symbol, startMoney, uninvestedMoney):
        self.stockSymbol = symbol
        self.startMoney = startMoney
        self.uninvestedMoney = uninvestedMoney
        self.investedMoney = self.startMoney - self.uninvestedMoney

    # Gets current price of a stock
    def currentPrice(self):
        r = requests.get("https://finnhub.io/api/v1/quote?symbol=%s&token=bvgkg9f48v6oab530peg" % self.stockSymbol)
        time.sleep(1)
        return r.json()["c"]

    def findStocksBought(self):
        stocksBought = self.investedMoney / self.currentPrice()
        try:
            f = open("savedInfo.json", "w")
        except:
            print("Check the name of the file")
            quit()
        else:
            data = {
                "stocksBought" : stocksBought,
                "uninvestedMoney" : self.uninvestedMoney
            }
            f.write(json.dumps(data))
            f.close()
        return stocksBought

    def divest(self, amount):
        if amount < self.investedMoney and amount > 0:
            self.uninvestedMoney += amount
            self.investedMoney -= amount
            self.findStocksBought()
        else:
            print("Check the amount you are trying to divest")

    def invest(self, amount):
        if amount < self.uninvestedMoney and amount > 0:
            self.uninvestedMoney -= amount
            self.investedMoney += amount
            self.findStocksBought()
        else:
            print("Check the amount you are trying to invest")

    def update(self):
        cp = self.currentPrice()
        self.investedMoney = self.findStocksBought() * cp
        totalMoney = self.investedMoney + self.uninvestedMoney
        gains = totalMoney - self.startMoney
        print("Starting Money: {} | Total Money: {} | Invested Money: {} | Uninvested Money: {} | Current Stock Price {} | Total Gains: {}"
            .format(self.startMoney, round(totalMoney, 2),
            round(self.investedMoney, 2), round(self.uninvestedMoney, 2),
            round(cp, 2), round(gains, 2)))