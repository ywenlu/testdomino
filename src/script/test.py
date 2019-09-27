import sys 
import csv
import json

""" arguments:
sys.argv[1],sys.argv[2]... 
"""

rows = { "diagnostic": None, "content": [] }

#print(sys.argv[1])

""" with open('C:/Users/alemercier/Documents/sherlock-ui/prix_vente_immobilier.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        rows["content"].append(row)
    rows["diagnostic"] = ["okoko"]
    print(json.dumps(rows)) """

sys.stdout.flush()