import json
from Simulator import Simulator
from Predicter import Predicter

# Creates simulation object
sim = Simulator('SPY', 500, 0, False)

# Uncomment the next 2 lines to create graph with predictor object

# pd = Predicter(sim.historicalCandles()["t"], sim.historicalCandles()["c"], 1, 1, 5)
# pd.predictGraph()

# Forever loop to run sim
while True:
    sim.update()