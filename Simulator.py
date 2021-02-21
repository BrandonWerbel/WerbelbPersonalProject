import requests
import time
import json
from Predicter import Predicter

class Simulator:

    """
    Constructor method
    """
    def __init__(self, symbol, startMoney, uninvestedMoney, realtime=True):
        self.stockSymbol = symbol
        self.startMoney = startMoney
        self.uninvestedMoney = uninvestedMoney
        self.realtime = realtime
        self.investedMoney = self.startMoney - self.uninvestedMoney
        self.prevMoney = self.investedMoney + self.uninvestedMoney

        # First half of data is training data, second half is simulation data
        slicer = round(len(self.historicalCandles()["t"]) / 2)
        self.simTimeStamp = self.historicalCandles()["t"][slicer + 1]

        # Gets saved info from json file if exists
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
            # If json file doesn't exist (first time running sim) use findStocksBought method to convert invested money into stocks
            self.findStocksBought()

        self.predicter = Predicter(self.historicalCandles()["t"][:slicer], self.historicalCandles()["c"][:slicer], 1, 1, 5)

    """
    Gets current price of a stock
    """
    def currentPrice(self):
        r = requests.get("https://finnhub.io/api/v1/quote?symbol=%s&token=bvgkg9f48v6oab530peg" % self.stockSymbol)
        # I can only make calls to the API 60 times per second, so I wait 1 second after every call
        time.sleep(1)
        return r.json()["c"]

    """
    Gets price of stock in simulation
    """
    def simCurrentPrice(self):
        price = self.historicalCloses()[self.simTimeStamp]
        # Moves forward in sim 60 seconds (1 minute)
        self.simTimeStamp += 60
        return price

    """
    Gets historical candles from past 20 days
    """
    def historicalCandles(self):
        r = requests.get("https://finnhub.io/api/v1/stock/candle?symbol={}&resolution=1&from={}&to={}&token=bvgkg9f48v6oab530peg"
            .format(self.stockSymbol, round(time.time()) - (60 * 60 * 24 * 20), round(time.time())))
        # I can only make calls to the API 60 times per second, so I wait 1 second after every call
        time.sleep(1)
        return r.json()

    """
    Returns dictionary object with historical
    timestamps as keys and corresponding
    historical closes as values
    """
    def historicalCloses(self):
        candles = self.historicalCandles()
        closes = candles["c"]
        timestamps = candles["t"]
        closesDict = {timestamps[0] : closes[0]}
        for index in range(1, len(closes)):
            closesDict[timestamps[index]] = closes[index]
        return closesDict

    """
    Calculates how many stocks can be bought with the amount of money invested
    """
    def findStocksBought(self):
        # If the mode is real time, use realtime data for the price, otherwise, use simulated data
        if self.realtime:
            stocksBought = self.investedMoney / self.currentPrice()
        else:
            stocksBought = self.investedMoney / self.simCurrentPrice()
        
        # save how many stocks were bought in json file
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

    """
    Sell stocks
    """
    def divest(self, amount):
        # You can only divest if you've invested the given amount and the given amount is positive
        if amount <= self.investedMoney and amount >= 0:
            self.uninvestedMoney += amount
            self.investedMoney -= amount
            self.findStocksBought()
        else:
            print("Check the amount you are trying to divest")

    """
    Buy stocks
    """
    def invest(self, amount):
        # You can only invest if you have the given amount and the given amount is positive
        if amount <= self.uninvestedMoney and amount >= 0:
            self.uninvestedMoney -= amount
            self.investedMoney += amount
            self.findStocksBought()
        else:
            print("Check the amount you are trying to invest")

    """
    Uses Predictor object to determine whether it is best to buy or sell stocks currently
    """
    def decideInvestAmount(self, currentPrice):
        pv = self.predicter.predictValue()
        # invest if the predicted price is about the current one, otherwise, divest
        if pv > currentPrice:
            self.invest(self.uninvestedMoney)
        elif pv < currentPrice:
            self.divest(self.investedMoney)

    """
    1 cycle of simulation, run in script.py
    """
    def update(self):
        # Use realtime data or simulated data based on mode
        if self.realtime:
            cp = self.currentPrice()
        else:
            cp = self.simCurrentPrice()
        
        # update predictor with latest price and decide whether to invest or divest
        self.predicter.addRealValue(cp)
        self.decideInvestAmount(cp)

        # calculate many data points, which are later printed
        self.investedMoney = self.findStocksBought() * cp
        totalMoney = self.investedMoney + self.uninvestedMoney
        gains = totalMoney - self.startMoney
        deltaGains = totalMoney - self.prevMoney
        self.prevMoney = totalMoney

        # Giant print statement, basically what the user sees in console when script.py is run
        # All decimals are rounded to 2 decimal points
        print("Starting Money: {} | Total Money: {} | Invested Money: {} | Uninvested Money: {} | Current Stock Price {} | Total Gains: {} | Delta Gains: {}"
            .format(self.startMoney, round(totalMoney, 2),
            round(self.investedMoney, 2), round(self.uninvestedMoney, 2),
            round(cp, 2), round(gains, 2), round(deltaGains, 2)))