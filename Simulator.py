import requests
import time
import json

class Simulator:

    def __init__(self, symbol, startMoney, uninvestedMoney, realtime=True):
        self.stockSymbol = symbol
        self.startMoney = startMoney
        self.uninvestedMoney = uninvestedMoney
        self.realtime = realtime
        self.investedMoney = self.startMoney - self.uninvestedMoney
        self.prevInvestedMoney = self.investedMoney
        self.simTimeStamp = self.historicalCandles()["t"][0]

        try:
            f = open("savedInfo.json")
        except:
            print("Check the name of the file")
            quit()
        else:
            fileContents = f.read()
            f.close()

        if fileContents != '':
            self.stocksBought = json.loads(fileContents)["stocksBought"]
            self.investedMoney = self.stocksBought * self.currentPrice()
            self.uninvestedMoney = json.loads(fileContents)["uninvestedMoney"]
        else:
            self.findStocksBought()

    # Gets current price of a stock
    def currentPrice(self):
        r = requests.get("https://finnhub.io/api/v1/quote?symbol=%s&token=bvgkg9f48v6oab530peg" % self.stockSymbol)
        time.sleep(1)
        return r.json()["c"]

    def simCurrentPrice(self):
        price = self.historicalCloses()[self.simTimeStamp]
        self.simTimeStamp += 60
        time.sleep(1)
        return price

    def historicalCandles(self):
        r = requests.get("https://finnhub.io/api/v1/stock/candle?symbol={}&resolution=1&from={}&to={}&token=bvgkg9f48v6oab530peg".format(self.stockSymbol, round(time.time()) - (390 * 60), round(time.time())))
        time.sleep(1)
        return r.json()

    def historicalCloses(self):
        candles = self.historicalCandles()
        closes = candles["c"]
        timestamps = candles["t"]
        closesDict = {timestamps[0] : closes[0]}
        for index in range(1, len(closes)):
            closesDict[timestamps[index]] = closes[index]
        return closesDict

    def findStocksBought(self):
        if self.realtime:
            stocksBought = self.investedMoney / self.currentPrice()
        else:
            stocksBought = self.investedMoney / self.simCurrentPrice()
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
        if self.realtime:
            cp = self.currentPrice()
        else:
            cp = self.simCurrentPrice()
        self.investedMoney = self.findStocksBought() * cp
        totalMoney = self.investedMoney + self.uninvestedMoney
        gains = totalMoney - self.startMoney
        deltaGains = self.investedMoney - self.prevInvestedMoney
        self.prevInvestedMoney = self.investedMoney
        print("Starting Money: {} | Total Money: {} | Invested Money: {} | Uninvested Money: {} | Current Stock Price {} | Total Gains: {} | Delta Gains: {}"
            .format(self.startMoney, round(totalMoney, 2),
            round(self.investedMoney, 2), round(self.uninvestedMoney, 2),
            round(cp, 2), round(gains, 2), round(deltaGains, 2)))