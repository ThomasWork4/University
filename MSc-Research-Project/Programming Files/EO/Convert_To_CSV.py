import os
import csv
import itertools
with open("EO_Frequency_Results.txt", 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open("Logged_Results_EO.csv", 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
