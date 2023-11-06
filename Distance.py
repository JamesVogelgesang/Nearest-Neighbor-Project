import csv

# This opens the CSV file containing the distances between addresses
with open("CSVs/WGUPS Distance Table3.csv", encoding="utf-8-sig") as csv1:
    # This reads the CSV file
    csvDist = csv.reader(csv1)
    # This places values from CSV into csvDist (a list)
    csvDist = list(csvDist)


# Calculate distance b/t 2 address
# O(1) time complexity
# O(1) space complexity
def distCalc(rowVal, colVal):

    distance = csvDist[rowVal][colVal]

    # If dist is blank, the indices are switched to find the distance
    # (Looks for dist from B -> A, rather than A -> B)
    if distance == '':
        distance = csvDist[colVal][rowVal]

    return float(distance)

# print(distCalc(0,1))

# Opens and reads the CSV file, then places values into csvAdd
with open("CSVs/Addresses.csv", encoding="utf-8-sig") as csv2:
    csvAdd = csv.reader(csv2)
    csvAdd = list(csvAdd)  # make csv into a list to iterate through


# Get address from CSV file
# O(n) time
# O(1) space complexity
def getAddress(address):
    # If the address in column 3 exists, then the ID from column 1 is returned
    for row in csvAdd:
        if address in row[2]:
            return int(row[0])

# print(getAddress("3575 W Valley Central Station bus Loop"))
