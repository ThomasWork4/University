import os
import csv

directories = os.listdir()
new_file = open("WW_Frequency_Results.txt", "w")
for file in directories:
    if file.endswith(".py"):
        continue
    else:
        current_file = open(file, "r")
        for line in current_file:
            clean_line = line.replace("[", "").replace("]", "").replace("'", "")
            new_file.write(clean_line)
new_file.close()
                    
    
