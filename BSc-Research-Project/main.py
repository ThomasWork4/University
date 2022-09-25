import math
from itertools import islice


# FindPredictions function used to find the prediction values for the current frame
def FindPredictions(Line_Number):
    Prediction_List = []
    filename = open("FINALRESULTS.txt", "r")
    FirstFrame = []
    SecondFrame = []
    ThirdFrame = []
    Text_Lines = filename.readlines()
    # reverse the text file so that we can iterate backwards for previous frames
    ReversedLines = reversed(Text_Lines)
    EndFrameCount = 0
    StartFrameCount = 0
    # iterate through the reversed text file and split each line
    for LinePosition, Value in islice(enumerate(ReversedLines), Line_Number, len(Text_Lines)):
        Document_Value = Value.split()
        # if the line is "start frame" or "end-frame" increment it's counter otherwise ignore it"
        if Document_Value[0] == "start-frame":
            StartFrameCount += 1
            continue
        if Document_Value[0] == "end-frame":
            EndFrameCount += 1
            continue
        # add frame contents to its frame list
        if EndFrameCount == 1:
            FirstFrame.append((Document_Value[0], Document_Value[1]))
        if EndFrameCount == 2:
            SecondFrame.append((Document_Value[0], Document_Value[1]))
        if EndFrameCount == 3:
            ThirdFrame.append((Document_Value[0], Document_Value[1]))
        # if 3 frames have been passed, break the loop
        if StartFrameCount == 4:
            break

    # iterate through both first and second frame and find the closest positions and record the difference between them
    FirstSecondComparisonList = [("l", "l")] * (len(FirstFrame))
    ShortestDistances = [(1.0, 1.0)] * (len(FirstFrame))
    for idx, y in enumerate(FirstFrame):
        Shortest_Distance = 1.0e37
        for z in SecondFrame:
            Distance = math.sqrt(((float(y[0]) - float(z[0])) ** 2) + ((float(y[1]) - float(z[1])) ** 2))
            if Distance < Shortest_Distance:
                Shortest_Distance = Distance
                ShortestDistances[idx] = ((float(y[0]) - float(z[0])), (float(y[1]) - float(z[1])))
                FirstSecondComparisonList[idx] = z

    # iterate through second and third frame and find the closest positions
    SecondThirdComparisonList = [("l", "l")] * (len(FirstSecondComparisonList))
    for idx, a in enumerate(FirstSecondComparisonList):
        Shortest_Distance = 1.0e37
        for b in ThirdFrame:
            Distance = math.sqrt(((float(a[0]) - float(b[0])) ** 2) + ((float(a[1]) - float(b[1])) ** 2))
            if Distance < Shortest_Distance:
                Shortest_Distance = Distance
                SecondThirdComparisonList[idx] = b

    # add the difference between the first and second positions to the thirds closest position for a coordinate
    for idx, i in enumerate(SecondThirdComparisonList):
        D = ShortestDistances[idx]
        Calculate_x = float(i[0]) + float(D[0])
        Calculate_y = float(i[1]) + float(D[1])
        Prediction_List.append((Calculate_x, Calculate_y))
    return Prediction_List


# FindCurrentFrameLocations function used to find the current frame positions
def FindCurrentFrameLocations(StartPoint):
    CurrentFrame = []
    filename = open("FINALRESULTS.txt", "r")
    File_line = filename.readlines()
    end_frame_count = 0
    # starting from the provided frame, add current frame positions to location list
    for Each_Line in File_line[StartPoint:]:
        Position = Each_Line.split()
        if Position[0] == "start-frame":
            continue
        elif Position[0] == "end-frame":
            end_frame_count += 1
            if end_frame_count == 1:
                break
            else:
                continue
        else:
            CurrentFrame.append((Position[0], Position[1]))
    return CurrentFrame


LocationPredictionComparisonList = []
location = []
All_Accuracy = []
line_number = None
x = open("FINALRESULTS.txt", "r")
lines = x.readlines()
Start_Frame_Count = 0
FramePosition = None

def Input():
    while True:
        User_Input = int(input("For which frame would you like to see the predictions?  :"))
        try:
            if User_Input < 4:
                raise IndexError
            if User_Input > 12359:
                raise IndexError
        except IndexError:
            print("Frame number must be between 4 and 12359 so that we have enough prediction data")
            continue
        if 4 <= User_Input <= 12359:
            return User_Input

User_Input = Input()

for index1, another in enumerate(lines):
    DocumentValue = another.split()
    if DocumentValue[0] == "start-frame":
        Start_Frame_Count += 1
        if Start_Frame_Count == User_Input:
            FramePosition = index1 - 2
            break
    else:
        continue

for index, another in islice(enumerate(lines), FramePosition, len(lines)):
    FrameAccuracy = []
    DocumentValue = another.split()
    if DocumentValue[0] == "start-frame":
        continue
    if DocumentValue[0] == "end-frame":
        ReversedList = reversed(lines)
        DataForReversedList = lines[index + 2]
        for number, line in enumerate(ReversedList):
            if DataForReversedList in line:
                line_number = number
                location = FindCurrentFrameLocations(index + 1)
                prediction = FindPredictions(line_number)
                # compare the location and prediction lists and find the closest possible predictions
                # to each position in the current frame
                LocationPredictionComparisonList = [(1.0, 1.0)] * (len(location))
                for index2, CurrentPositions in enumerate(location):
                    shortest_distance = 1.0e37
                    for PredictionPositions in prediction:
                        distance = math.sqrt(
                            ((float(CurrentPositions[0]) - float(PredictionPositions[0])) ** 2) + (
                                    (float(CurrentPositions[1]) - float(PredictionPositions[1])) ** 2))
                        if distance < shortest_distance:
                            shortest_distance = distance
                            LocationPredictionComparisonList[index2] = PredictionPositions
                # output each frame position and it's prediction
                for index3, CurrentPositions in enumerate(location):
                    ItsPrediction = LocationPredictionComparisonList[index3]
                    XAccuracy = ((float(CurrentPositions[0]) - float(ItsPrediction[0])) / float(
                        CurrentPositions[0])) * 100
                    YAccuracy = ((float(CurrentPositions[1]) - float(ItsPrediction[1])) / float(
                        CurrentPositions[1])) * 100
                    Acc = abs((XAccuracy + YAccuracy) / 2)
                    Accuracy = (100 - Acc)
                    All_Accuracy.append(Accuracy)
                    FrameAccuracy.append(Accuracy)
                    print("The position ", CurrentPositions, " in frame no.", User_Input, " was predicted to be ",
                          ItsPrediction)
                    print("This prediction is ", round(Accuracy, 2), "% Accurate")

        FrameAccuracyTotal = sum(FrameAccuracy) / len(FrameAccuracy)
        print("The overall accuracy of the predictions in frame no.", User_Input, " is ", round(FrameAccuracyTotal, 2), "%")
        break

# GlobalAccuracy = sum(All_Accuracy) / len(All_Accuracy)
# print("The overall accuracy of this program is ", GlobalAccuracy, "%")
