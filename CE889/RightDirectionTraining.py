import csv

def Extract_Right_data():
    newfile = open("RightDirectionTraining.csv", "w", newline="")
    writer = csv.writer(newfile)
    with open("ce889_dataCollection.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if float(row[0]) > 0:
                writer.writerow([row[0], row[1], row[2], row[3]])
    newfile.close()

def Split_Normalize_data():
    xMin = 0
    xMax = 0
    yMin = 0
    yMax = 0
    #Initialize lists to store training values 
    newfile = open("Training_file.csv", "w", newline="")
    newfile2 = open("Validation_file.csv", "w", newline="")
    writer = csv.writer(newfile)
    writer2 = csv.writer(newfile2)
    Columns = []
    X_Distance_to_target = []
    Y_Distance_to_target = []
    Expected_val_X = []
    Expected_val_Y = []
    # Open the training set and sort each value into its subsequent list 
    with open("RightDirectionTraining.csv") as csv_file:
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
    # For each column of data, normalize the data and add it to the new csv file 
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
    splitpoint = round(len(Expected_val_X) * 0.7)
    for x in range(len(Expected_val_X)):
        if x < splitpoint:
            writer.writerow([Columns[0][x], Columns[1][x], Columns[2][x], Columns[3][x]])
        else:
            writer2.writerow([Columns[0][x], Columns[1][x], Columns[2][x], Columns[3][x]])
    newfile.close()
    newfile2.close()
    return xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax

Extract_Right_data()
xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax = Split_Normalize_data()
#print(xMin, xMax, yMin, yMax, OutputxMin, OutputxMax, OutputyMin, OutputyMax)
