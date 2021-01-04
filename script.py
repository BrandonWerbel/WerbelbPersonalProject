import json
from Simulator import Simulator
from Predicter import Predicter

sim = Simulator('SPY', 500, 0, False)

# pd = Predicter(sim.historicalCandles()["t"], sim.historicalCandles()["c"], 1, 1, 5)
# pd.predictGraph()

while True:
    sim.update()