import requests
import time
import json
from Predicter import Predicter

class Simulator:

    def __init__(self, symbol, startMoney, uninvestedMoney, realtime=True):
        self.stockSymbol = symbol
        self.startMoney = startMoney
        self.uninvestedMoney = uninvestedMoney
        self.realtime = realtime
        self.investedMoney = self.startMoney - self.uninvestedMoney
        self.prevMoney = self.investedMoney + self.uninvestedMoney

        slicer = round(len(self.historicalCandles()["t"]) / 2)
        self.simTimeStamp = self.historicalCandles()["t"][slicer + 1]

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

        self.predicter = Predicter(self.historicalCandles()["t"][:slicer], self.historicalCandles()["c"][:slicer], 1, 1, 5)

    # Gets current price of a stock
    def currentPrice(self):
        r = requests.get("https://finnhub.io/api/v1/quote?symbol=%s&token=bvgkg9f48v6oab530peg" % self.stockSymbol)
        time.sleep(1)
        return r.json()["c"]

    def simCurrentPrice(self):
        price = self.historicalCloses()[self.simTimeStamp]
        self.simTimeStamp += 60
        return price

    def historicalCandles(self):
        r = requests.get("https://finnhub.io/api/v1/stock/candle?symbol={}&resolution=1&from={}&to={}&token=bvgkg9f48v6oab530peg"
            .format(self.stockSymbol, round(time.time()) - (60 * 60 * 24 * 20), round(time.time())))
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
        if amount <= self.investedMoney and amount >= 0:
            self.uninvestedMoney += amount
            self.investedMoney -= amount
            self.findStocksBought()
        else:
            print("Check the amount you are trying to divest")

    def invest(self, amount):
        if amount <= self.uninvestedMoney and amount >= 0:
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
        self.predicter.addRealValue(cp)
        self.decideInvestAmount(cp)

        self.investedMoney = self.findStocksBought() * cp
        totalMoney = self.investedMoney + self.uninvestedMoney
        gains = totalMoney - self.startMoney
        deltaGains = totalMoney - self.prevMoney
        self.prevMoney = totalMoney

        print("Starting Money: {} | Total Money: {} | Invested Money: {} | Uninvested Money: {} | Current Stock Price {} | Total Gains: {} | Delta Gains: {}"
            .format(self.startMoney, round(totalMoney, 2),
            round(self.investedMoney, 2), round(self.uninvestedMoney, 2),
            round(cp, 2), round(gains, 2), round(deltaGains, 2)))

    def decideInvestAmount(self, currentPrice):
        pv = self.predicter.predictValue()
        if pv > currentPrice:
            self.invest(self.uninvestedMoney)
        elif pv < currentPrice:
            self.divest(self.investedMoney)