from matplotlib import pyplot
from statsmodels.tsa.arima.model import ARIMA

class Predicter:
    def __init__(self, x_list, y_list, p, q, d):
        print("Creating Predicter object")

        # Slicer is variable that determines where to separate the training data from the real data
        slicer = 0.95

        self.x_list = x_list
        self.x_train = x_list[:round(len(x_list) * slicer)]
        self.x_real = x_list[round(len(x_list) * slicer):]

        self.y_list = y_list
        self.y_train = y_list[:round(len(y_list) * slicer)]
        self.y_real = y_list[round(len(y_list) * slicer):]


        self.model = ARIMA(self.y_list, order=(p,q,d)).fit()
        self.training_model = ARIMA(self.y_train, order=(p,q,d)).fit()
        print("Made models")

    """
    Predicts the next value
    """
    def predictValue(self):
        return self.model.forecast(steps=1)[0]

    """
    Adds real value to ARIMA model
    """
    def addRealValue(self, realValue):
        self.model = self.model.append([realValue])

    """
    Creates graph plotting the predicted values from the ARIMA model against the real data
    """
    def predictGraph(self):
        # Iterates through real data, predicting a value, then adding the actual one to the model
        forecast = []
        for y in self.y_real:
            forecast.append(self.training_model.forecast(steps=1)[0])
            self.training_model = self.training_model.append([y])
        print("get forecast")

        # Plots 2 graphs
        pyplot.plot(range(0, len(forecast)), forecast, label="Forecast")
        pyplot.plot(range(0, len(forecast)), self.y_real[:len(forecast)])
        pyplot.legend()

        pyplot.show()

        return forecast