import math
from CE889NeuralNetwork import Neuron
from CE889NeuralNetwork import feedforward_process
from CE889NeuralNetwork import Load_Weights

class NeuralNetHolder:
    def __init__(self):
        super().__init__()
        
        Input_W = Load_Weights("I")
        Hidden_W = Load_Weights("H")

        input_layer = [Neuron(0, Input_W[0], 0, 4), Neuron(0, Input_W[1], 1, 4), Neuron(1, Input_W[2], 2, 4)]
        hidden_layer = [Neuron(0, Hidden_W[0], 0, 2), Neuron(0, Hidden_W[1], 1, 2), Neuron(0, Hidden_W[2], 2, 2), Neuron(0, Hidden_W[3], 3, 2), Neuron(0, Hidden_W[4], 4, 2), Neuron(1, Hidden_W[4], 5, 2)]
        output_layer = [Neuron(0, [0], 0, 1), Neuron(0, [0], 1, 1)]

    def predict(self, input_row):
        xMin = -803.4449940466636
        xMax = 798.537803504677
        yMin = 65.012
        yMax = 673.916
        OutputxMin = -4.675848637640493
        OutputxMax = 7.998124507989192
        OutputyMin = -7.0874858159870096
        OutputyMax = 7.071662013241951
        PreData = input_row.split(",")
        Normalizedx = ((float(PreData[0]) - xMin) / (xMax - xMin))
        Normalizedy = ((float(PreData[1]) - yMin) / (yMax - yMin))
        Data = (Normalizedx, Normalizedy)
        Results = feedforward_process(Data)
        VelX = (Results[0] * (OutputxMax - OutputxMin)) + OutputxMin
        VelY = (Results[1] * (OutputyMax - OutputyMin)) + OutputyMin
        return (VelX, VelY)


