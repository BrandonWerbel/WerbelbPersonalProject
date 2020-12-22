import json
from Simulator import Simulator

sim = Simulator('SPY', 500, 50)

try:
    f = open("savedInfo.json")
except:
    print("Check the name of the file")
    quit()
else:
    fileContents = f.read()
    f.close()

if fileContents != '':
    sim.stocksBought = json.loads(fileContents)["stocksBought"]
    sim.investedMoney = sim.stocksBought * sim.currentPrice()
    sim.uninvestedMoney = json.loads(fileContents)["uninvestedMoney"]
else:
    sim.findStocksBought()

while True:
    sim.update()