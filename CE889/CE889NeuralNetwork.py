import random
import math
import csv

class Neuron:
    def __init__(self, activation_value, weights, neuron_index, delta_weights):
        self.activation_value = activation_value
        self.weights = weights
        self.neuron_index = neuron_index
        self.gradient_value = 0
        counter = 0
        self.delta_weights = [0] * delta_weights
            
    def weight_multiplication(self, previous_layer):
        result = 0
        # for every neuron in the previous layer attached to the current neuron sum their (weight * activation value)
        for x in range(len(previous_layer)):
            result += (previous_layer[x].activation_value) * (previous_layer[x].weights[self.neuron_index])
        # Sigmoid activation function of the result makes the new activation value of the current neuron
        self.activation_value = 1/(1 + math.exp(-result))
        
def Split_Normalize_data():
    xMin = 0
    xMax = 0
    yMin = 0
    yMax = 0
    #Initialize lists to store training and validation values 
    newfile = open("Training_file.csv", "w", newline="")
    newfile2 = open("Validation_file.csv", "w", newline="")
    writer = csv.writer(newfile)
    writer2 = csv.writer(newfile2)
    Columns = []
    X_Distance_to_target = []
    Y_Distance_to_target = []
    Expected_val_X = []
    Expected_val_Y = []
    
    # Open the dataset and store each row value into its respective list 
    with open("ce889_dataCollection.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            X_Distance_to_target.append(row[0])
            Y_Distance_to_target.append(row[1])
            Expected_val_X.append(row[2])
            Expected_val_Y.append(row[3])
    Columns.append(X_Distance_to_target)
    Columns.append(Y_Distance_to_target)
    Columns.append(Expected_val_X)
    Columns.append(Expected_val_Y)
    
    # For each column of data, normalize each data value and add it to a new csv file
    for x in Columns:
        Max = None
        Min = None
        Max = float(x[0])
        Min = float(x[0])
        for i in x:
            if float(i) > Max:
                Max = float(i)
            elif float(i) < Min:
                Min = float(i)
            else:
                continue
        #Store Min, Max values for each column to be used in prediction function
        if Columns.index(x) == 0:
            xMin = Min
            xMax = Max
        elif Columns.index(x) == 1:
            yMin = Min
            yMax = Max
        elif Columns.index(x) == 2:
            OutputxMin = Min
            OutputxMax = Max
        elif Columns.index(x) == 3:
            OutputyMin = Min
            OutputyMax = Max
        for i in range(len(x)):
            new = (float(x[i]) - Min) / (Max - Min)
            x[i] = new
    # Split the dataset as follows: 70% Training Set, 30% Validation Set
    splitpoint = round(len(Expected_val_X) * 0.7)
    for x in range(len(Expected_val_X)):
        if x < splitpoint:
            writer.writerow([Columns[0][x], Columns[1][x], Columns[2][x], Columns[3][x]])
        else:
            writer2.writerow([Columns[0][x], Columns[1][x], Columns[2][x], Columns[3][x]])
    newfile.close()
    newfile2.close()
    return xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax

        
def feedforward_process(input_list):
    # make the inputs the activation values of the input neurons
    for x in range(len(input_layer)-1):
        input_layer[x].activation_value = input_list[x]
    # apply weight multiplication for each neuron in the hidden layer and output layer
    # but make sure the activation value of the bias doesn't change from 1
    for x in range(len(hidden_layer) - 1):
        hidden_layer[x].weight_multiplication(input_layer)

    for x in range(len(output_layer)):
        output_layer[x].weight_multiplication(hidden_layer)
    return (output_layer[0].activation_value, output_layer[1].activation_value)
    # return the result of the neural network 


def Backpropagation(outputs, learning_rate):
    lambda1 = 0.8
    momentum = 0.2
    error = [0, 0]
    # find the error for each output value
    for x in range(len(outputs)):
        error[x] = outputs[x] - output_layer[x].activation_value

    # find the gradient_value for each output layer neuron
    for x in range(len(output_layer)):
        output_layer[x].gradient_value = lambda1 * output_layer[x].activation_value * (1 - output_layer[x].activation_value) * error[x]

    #values to multiply at the end of the next equation
    List_Of_Values = [0] * len(hidden_layer)
    for x in range(len(hidden_layer)):
        for i in range(len(output_layer)):
            List_Of_Values[x] = List_Of_Values[x] +(output_layer[i].gradient_value * hidden_layer[x].weights[i])

    # find the gradient_value for each hidden neuron 
    for x in range(len(hidden_layer)):
        hidden_layer[x].gradient_value = lambda1 * hidden_layer[x].activation_value * (1 - hidden_layer[x].activation_value) * List_Of_Values[x]

    # find the delta weights for all hidden neuron
    for x in range(len(hidden_layer)):
        for i in range(len(hidden_layer[x].delta_weights)):
            hidden_layer[x].delta_weights[i] = learning_rate * output_layer[i].gradient_value * hidden_layer[x].activation_value + momentum * hidden_layer[x].delta_weights[i]

    # find the delta weights for all input neurons
    for x in range(len(input_layer)):
        for i in range(len(input_layer[x].delta_weights)):
            input_layer[x].delta_weights[i] = learning_rate * hidden_layer[i].gradient_value * input_layer[x].activation_value + momentum * input_layer[x].delta_weights[i]

    # update the weights for all hidden neurons
    for x in range(len(hidden_layer)):
        for i in range(len(hidden_layer[x].weights)):
            hidden_layer[x].weights[i] = hidden_layer[x].weights[i] + hidden_layer[x].delta_weights[i]

    # update the weights for all input neurons
    for x in range(len(input_layer)):
        for i in range(len(input_layer[x].weights)):
            input_layer[x].weights[i] = input_layer[x].weights[i] + input_layer[x].delta_weights[i]


def Training_Function(Input_List, Output_List, Validation_Input, Validation_Output, epochs):
    T_Data_Collection = []
    V_Data_Collection = []
    Minimum = math.inf
    counter = 0
    Global_Minima = math.inf
    Previous_VRMSE = []
    for i in range(epochs):
        Training_Error = 0
        Validation_Error = 0
        # for each line in the training data, feedforward and backpropogate
        # to calculate optimal weights which are then saved 
        for x in range(len(Input_List)):
            feedforward_process([Input_List[x][0], Input_List[x][1]])
            Backpropagation([Output_List[x][0], Output_List[x][1]], 0.05)

        # Calculate Training error 
        for x in range(len(Input_List)):
            Result = feedforward_process([Input_List[x][0], Input_List[x][1]])
            PreError1 = Result[0] - Output_List[x][0]
            PreError2 = Result[1] - Output_List[x][1]
            Error = ((PreError1 + PreError2) ** 2) / 2
            Training_Error += Error 
        Training_Error = Training_Error / len(Input_List)
        RMSE = math.sqrt(Training_Error)
        T_Data_Collection.append(RMSE)

        # Calculate Validation error
        for x in range(len(Validation_Input)):
            VResult = feedforward_process([Validation_Input[x][0], Validation_Input[x][1]])
            VPreError1 = VResult[0] - Validation_Output[x][0]
            VPreError2 = VResult[1] - Validation_Output[x][1]
            VError = ((VPreError1 + VPreError2) ** 2) / 2
            Validation_Error += VError 
        Validation_Error = Validation_Error / len(Input_List)
        Validation_RMSE = math.sqrt(Validation_Error)
        print("Epoch: ", i, " RMSE TE: ", round(RMSE, 5) ,"RMSE VE: ", round(Validation_RMSE, 5))

        # Patience as opposed to exhaustive (because if we were working with images exhaustive would take too long
        # We initalize a counter that increments every time a subsequent validation RMSE value has gone up and
        # Resets everytime it goes down. If we have 5 increases in a row, then we save the weights from the lowest
        # Validation error we've had and apply them to the neural network
        V_Data_Collection.append(Validation_RMSE)
        if Validation_RMSE < Global_Minima:
            I_weights = []
            H_weights = []
            counter = 0
            Global_Minima = Validation_RMSE
            for x in input_layer:
                weights = []
                for i in x.weights:
                    weights.append(i)
                I_weights.append(weights)
            for x in hidden_layer:
                weights = []
                for i in x.weights:
                    weights.append(i)
                H_weights.append(weights)
        elif Validation_RMSE < V_Data_Collection[-2]:
            counter = 0
            pass
        elif Validation_RMSE > V_Data_Collection[-2] or Validation_RMSE == V_Data_Collection[-2]:
            counter += 1
            if counter == 5:
                for x in range(len(input_layer)):
                    input_layer[x].weights = I_weights[x]
                for x in range(len(hidden_layer)):
                    hidden_layer[x].weights = H_weights[x]
                break
            else:
                continue

    # Uncomment to save the Error values in an excel file for visualization         
    newfile = open("Error_Storage.csv", "w", newline="")
    writer = csv.writer(newfile)
    for x in range(len(V_Data_Collection)):
        writer.writerow([T_Data_Collection[x], V_Data_Collection[x]])
    newfile.close()
        
        
        
    
def Save_Weights():
    # Save all the weights after the network is trained to a text file 
    with open("Saved_Weights.txt", "w") as file:
        for x in input_layer:
            weights = ""
            for i in x.weights:
                weights = weights + str(i) + " "
            file.write("Input " + weights + "\n")
        for x in hidden_layer:
            weights = ""
            for i in x.weights:
                weights = weights + str(i) + " "
            file.write("Hidden " + weights + "\n")


def Initialize_Random_Weights(Number):
    # Call with a specified number to create equal length list of random weights
    Weights = []
    if Number == 0:
        Weights = [0]
    else:
        for x in range(Number):
            Weights.append(random.uniform(-1, 1))
    return Weights
    

def Load_Weights(Choice):
    # Load the weights of all the input neurons in the form of a list of lists 
    input_Layer_Weights = []
    hidden_Layer_Weights = []
    with open("Saved_Weights.txt", "r") as file:
        for line in file:
            SplitLine = line.split()
            if SplitLine[0] == "Input":
                Neuron_Weights = []
                for x in SplitLine:
                    if x != "Input":
                        Neuron_Weights.append(float(x))
                input_Layer_Weights.append(Neuron_Weights)
            elif SplitLine[0] == "Hidden":
                Neuron_Weights = []
                for x in SplitLine:
                    if x != "Hidden":
                        Neuron_Weights.append(float(x))
                hidden_Layer_Weights.append(Neuron_Weights)
    if Choice == "I":
        return input_Layer_Weights
    elif Choice == "H":
        return hidden_Layer_Weights

#5 Neurons
#input_layer = [Neuron(0, Initialize_Random_Weights(5), 0, 5), Neuron(0, Initialize_Random_Weights(5), 1, 5), Neuron(4, Initialize_Random_Weights(5), 2, 5)]
#hidden_layer = [Neuron(0, Initialize_Random_Weights(2), 0, 2), Neuron(0, Initialize_Random_Weights(2), 1, 2), Neuron(0, Initialize_Random_Weights(2), 2, 2), Neuron(0, Initialize_Random_Weights(2), 3, 2), Neuron(0, Initialize_Random_Weights(2), 4, 2), Neuron(1, Initialize_Random_Weights(2), 5, 2)]
#output_layer = [Neuron(0, Initialize_Random_Weights(0), 0, 1), Neuron(0, Initialize_Random_Weights(0), 1, 1)]


#SW
Input_W = Load_Weights("I")
#SW
Hidden_W = Load_Weights("H")
#SW
input_layer = [Neuron(0, Input_W[0], 0, 5), Neuron(0, Input_W[1], 1, 5), Neuron(1, Input_W[2], 2, 5)]
#SW
hidden_layer = [Neuron(0, Hidden_W[0], 0, 2), Neuron(0, Hidden_W[1], 1, 2), Neuron(0, Hidden_W[2], 2, 2), Neuron(0, Hidden_W[3], 3, 2), Neuron(0, Hidden_W[4], 4, 2), Neuron(1, Hidden_W[4], 5, 2)]
#SW
output_layer = [Neuron(0, Initialize_Random_Weights(0), 0, 1), Neuron(0, Initialize_Random_Weights(0), 1, 1)]


# Splitting and storing all data values into validation and training files and lists
# Storing all the maximum and minumum values used to normalize the output columns
Training_Inputs = []
Training_Outputs = []
Validation_Inputs = []
Validation_Outputs = []
xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax = Split_Normalize_data()
#print(xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax)

with open("Training_file.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        Training_Inputs.append((float(row[0]), float(row[1])))
        Training_Outputs.append((float(row[2]), float(row[3])))
with open("Validation_file.csv") as csv_file:
    csv_reader = csv.reader(csv_file)
    line_count = 0
    for row in csv_reader:
        Validation_Inputs.append((float(row[0]), float(row[1])))
        Validation_Outputs.append((float(row[2]), float(row[3])))

#Training_Function(Training_Inputs, Training_Outputs, Validation_Inputs, Validation_Outputs, 1000)
#Save_Weights()


    
    
