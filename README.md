# WerbelbPersonalProject

## Journels

### 12/22/2020

> Today was my first day of actual coding, and I got quite a bit done. After a couple of days trying to find a free API I could use to get data from the stock market, I finally found "finnhub.io" at the end of yesterday, and was able to start experimenting with it today. Using this data, I was able to create a simulation of the SPDR S&P 500 Trust ETF (SPY), an ETF tracking the S&P 500. In my simulation, I can start with a certain amount of total money (I've been using $500), of which I can invest a certain amount in the ETF. The simulation updates every second, at which time it finds the current price of a single stock in the ETF and uses that to calculate the total amount of money I have right now as well as my total gains from the start of the simulation. I then made invest and divest methods I can use to put in or take money from the ETF, which changes the amount of risk and reward possible. One part of this simulation I am especially proud of is my "savedInfo.json" file, which allows me to stop and start the simulation and not lose any progress. Hopefully during my next session, I will be able to start programming the ML necessary to determine the best times to invest and divest.
