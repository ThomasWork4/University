import os

# JSONReader function breaks each data line up using the surrounding braces
def JSONReader(Filename):
    x = open(Filename, "r+")
    o = open("Cleanup.txt", "w")
    for y in x:
        for z in y:
            if z == "{":
                o.write("\n{")
            else:
                o.write(z)
    x.close()
    o.close()

# Simple function deletes are useless metadata including punction and misc information
def Simple(Filename):
    x = open(Filename, "r+")
    j = open("NumbersOnly.txt", "w")
    delete_list = ["image_id", "category_id", ": 1", "keypoints", "{", "}", ":", '"', "1,  ", ",",".jpg","score", "[", "]"]
    for y in x:
        for c in delete_list:
            y = y.replace(c, "")
        j.write(y)
    x.close()
    j.close()

# Obtain function splits each line into a list and retrives the ankle locations 
def Obtain(Filename):
    x = open(Filename, "r")
    a = x.readlines()
    x.close()
    j = open("FeetValues.txt", "w")
    for aline in a:
        if aline.strip("\n") != "":
            values = aline.split()
            x1 = values[0] + " " + values[46] + " " + values[47] + " " + values[49] + " " + values[50] + "\n"
            j.write(x1)
    j.close()

# Final function calculates a center of mass and limits positions to within the court
def Final(Filename) :
    x = open(Filename, "r")
    j = open("CenterOfMass.txt", "w")
    for aline in x:
        new = aline.split()
        FinalX = (float(new[1]) + float(new[3])) / 2
        FinalY = (float(new[2]) + float(new[4])) / 2
        if FinalY > 130 and FinalY < 315 :
            j.write(new[0] + " " + str(FinalX) + " " + str(FinalY) + "\n")
    x.close()
    j.close()

# ReformatWithFrame function adds frame markers to each frame
def ReformatWithFrame(Filename):
    x = open(Filename, "r")
    j = open("FINALRESULTS2.txt", "w+")
    FrameCount = 0
    for aline in x:
        values = aline.split()
        if values[0] != FrameCount:
            j.write("end-frame" + "\n")
            j.write("start-frame" + "\n")
            j.write(values[1] + " " + values[2] + "\n")
            FrameCount = values[0]
        else:
            j.write(values[1] + " " + values[2] + "\n")
    x.close()
    j.close()
    # Removes the first line of the text file as the end frame marker is redundant
    y = open('FINALRESULTS2.txt', 'r')
    data = y.read().splitlines(True)
    z = open('FINALRESULTS.txt', 'w')
    z.writelines(data[1:])
    y.close()
    z.close()

# Calls all functions in order of execution 
JSONReader("VolleyBall.json")
Simple("Cleanup.txt")
Obtain("NumbersOnly.txt")
Final("FeetValues.txt")
ReformatWithFrame("CenterOfMass.txt")

# Removes all text files from directory as they are no longer of use
# These can be hashed out if progress of cleanup needs to be checked
os.remove("Cleanup.txt")
os.remove("NumbersOnly.txt")
os.remove("FeetValues.txt")
os.remove("CenterOfMass.txt")
os.remove("FINALRESULTS2.txt")


