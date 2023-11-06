import csv
import datetime
import re

import Distance
from HashTable import HashTable
from Package import Package
from Truck import Truck


# Function to load packages into hash table, packageHash
# O(n) time and space complexity
def loadPackageData(filename):
    with open(filename, encoding="utf-8-sig") as packages:
        packageData = csv.reader(packages)
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZip = package[4]
            pDeliveryDeadline = package[5]
            pWeight = package[6]
            pStatus = "At the hub"

            # Create package object
            package = Package(pID, pAddress, pCity, pState, pZip, pDeliveryDeadline, pWeight, pStatus)

            # Inserts package into packageHash
            packageHash.insert(pID, package)


# Nearest neighbor algorithm
# This determines the shortest path from the truck's current location to whichever package loaded onto the truck is closest
# O(n^2) time
# O(n) space complexity
def nearestNeighbor(truck):
    # Add all packages in remainingPackages list
    remainingPackagesList = []

    for ID in truck.packages:
        package = packageHash.lookUp(ID)
        remainingPackagesList.append(package)

    # print([str(item) for item in remainingPackages]) # Checks if packages are being loaded into remainingPackages

    # clear truck.packages list, in order to enter them in order according to nearestNeighbor algorithm
    truck.packages.clear()

    # Iterates through remainingPackages list to find the next stop for the truck
    while len(remainingPackagesList) > 0:
        nPackage = None
        nLocation = 500.0

        # compare current location to distances to all remaining packages' addresses, and choose the shortest dist
        for package in remainingPackagesList:
            distance = float(Distance.distCalc(Distance.getAddress(truck.currentAddress), Distance.getAddress(package.address)))
            if distance <= nLocation:
                nLocation = distance
                nPackage = package

        # adds nearest neighbor to truck.packages
        truck.packages.append(nPackage.ID)

        # adds miles driven to the milesTravelled attribute
        truck.milesTravelled += float(nLocation)

        # gives truck its next address
        truck.currentAddress = nPackage.address

        # totalTime is calculated using the total miles driven so far divided by the truck's speed
        truck.totalTime += datetime.timedelta(hours=nLocation / 18)

        # determines the time that each package is delivered
        nPackage.timeDelivered = truck.startTime + truck.totalTime

        # removes delivered package from remainingPackages
        remainingPackagesList.remove(nPackage)

# Creates hash table
packageHash = HashTable()

# Loads package data into packageHash
loadPackageData("CSVs/WGUPS Package File - tfCSV.csv")


# Check if data is being loaded into packageHash
# for i in range(len(packageHash.table) + 1):
# print("Package: {}".format(packageHash.lookUp(i + 1)))


# Create 3 truck objects
t1 = Truck(16, 18, datetime.timedelta(days=0, hours=8), 0.0, [10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 29, 30, 31], "4001 South 700 East", datetime.timedelta(hours=0.0))
t2 = Truck(16, 18, datetime.timedelta(days=0, hours=9, minutes=5), 0.0, [1, 2, 3, 6, 18, 25, 28, 32, 34, 35, 36, 37, 38, 39, 40],
           "4001 South 700 East", datetime.timedelta(hours=0.0))
t3 = Truck(16, 18, datetime.timedelta(days=0, hours=10, minutes=44), 0.0, [4, 5, 7, 8, 9, 17, 26, 27, 33], "4001 South 700 East",
           datetime.timedelta(hours=0.0))

# Put each truck through the nearest neighbor function
nearestNeighbor(t1)
nearestNeighbor(t2)
nearestNeighbor(t3)


# Creates a truck list
trucks = [t1, t2, t3]


# Uses the truck list and a given package ID to find out which truck the package is on
# This will be used to get the starting time of the truck, which helps in calculating time delivered for each package
# O(n) time complexity
# O(1) space complexity
def findTruck(pID, trucks):
    # Searches trucks list
    for truck in trucks:
        if pID in truck.packages:
            # if pID found
            return truck
    # if pID is not found
    return None


# NO LONGER USED
# Determines status of package after considering user-entered time range
# Used to complete Task 2, D.1 - D.3
# Not a user function! (that's why I don't display the option)
# Time complexity of O(n)
# O(1) space complexity
def packStatus(truck):
    # take time 1 as input
    time1 = input("What is the start time?")

    # time1 is compared to stringFormat
    stringFormat = r'^\d{2}:\d{2}:\d{2}$'

    # re.match() is used to see if time1 is in the expected format
    if not re.match(stringFormat, time1):
        print("Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time")

    else:

        # if time1 is in expected format, split and store the hour/min/sec
        hours1, minutes1, seconds1 = map(int, time1.split(':'))

        # convert to timedelta
        userDeltaTime1 = datetime.timedelta(hours=hours1, minutes=minutes1, seconds=seconds1)

        # take time 2 as input
        time2 = input("What is the end time?")

        # time2 is compared to stringFormat
        stringFormat = r'^\d{2}:\d{2}:\d{2}$'

        # re.match() is used to see if time2 is in the expected format
        if not re.match(stringFormat, time2):
            print("Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time")

        else:
            # if time1 is in expected format, split and store the hour/min/sec
            hours2, minutes2, seconds2 = map(int, time2.split(':'))

            # convert to timedelta
            userDeltaTime2 = datetime.timedelta(hours=hours2, minutes=minutes2, seconds=seconds2)

            # search the list of packages the truck has
            for packageID in truck.packages:
                package = packageHash.lookUp(packageID)
                # If the end time of user-entered range is before the truck the package is on has started, then package status is "at hub"
                if truck.startTime > userDeltaTime2:
                    print("Package ID: " + str(packageID) + "\nPackage Status: At hub")
                # If the truck has started, then need to determine if delivered or en route
                elif truck.startTime <= userDeltaTime2:
                    # The time of delivery is compared to end range of user-entered time.
                    if package.timeDelivered > userDeltaTime2:
                        print("Package ID: " + str(package.ID) + "\nPackage Status: En Route")
                    else:
                        print("Package ID: " + str(package.ID) + "\nPackage Status: Delivered at " + str(package.timeDelivered))


# Determines the statuses of every package at a certain point in time
def allPackageStatus():
    # user entered start time
    timeStart = input("What is the start time?")

    # this is the expected user input format
    stringFormat = r'^\d{2}:\d{2}:\d{2}$'

    # re.match() is used to see if timeStart is in the expected format
    if not re.match(stringFormat, timeStart):
        print(
            "Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time")

    else:

        # if timeStart is in expected format, split and store the hour/min/sec
        hours1, minutes1, seconds1 = map(int, timeStart.split(':'))

        # convert to timedelta
        userDeltaTime1 = datetime.timedelta(hours=hours1, minutes=minutes1, seconds=seconds1)

        # take timeEnd as input
        timeEnd = input("What is the end time?")

        # time2 is compared to stringFormat
        stringFormat = r'^\d{2}:\d{2}:\d{2}$'

        # re.match() is used to see if time2 is in the expected format
        if not re.match(stringFormat, timeEnd):
            print(
                "Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time")

        else:
            # if time1 is in expected format, split and store the hour/min/sec
            hours2, minutes2, seconds2 = map(int, timeEnd.split(':'))

            # convert to timedelta
            userDeltaTime2 = datetime.timedelta(hours=hours2, minutes=minutes2, seconds=seconds2)

            # search the list of packages the truck has
            for truck in trucks:
                for packageID in truck.packages:
                    package = packageHash.lookUp(packageID)
                    # If the end time of user-entered range is before the truck the package is on has started, then package status is "at hub"
                    if truck.startTime > userDeltaTime2:
                        print("Package ID: " + str(packageID) + "\nPackage Status: At hub\nTo be delivered at: " + str(package.timeDelivered))
                    # If the truck has started, then need to determine if delivered or en route
                    elif truck.startTime <= userDeltaTime2:
                        # The time of delivery is compared to end range of user-entered time.
                        if package.timeDelivered > userDeltaTime2:
                            print("Package ID: " + str(package.ID) + "\nPackage Status: En Route\nTo be delivered at: " + str(package.timeDelivered))
                        else:
                            print("Package ID: " + str(package.ID) + "\nPackage Status: Delivered at " + str(
                                package.timeDelivered))


# This is the lookup function for Problem B
# This function will take user inputted ID, and return package ID, address, deadline, city, zip, weight, and time of delivery
# Time complexity is O(n)
# Space complexity is O(1)
def lookup(pID):
    package = packageHash.lookUp(pID)

    userTime = input(
        "Please provide the time in which you are interested in using military time (24-hour clock) and the format HH:MM:SS: \n")

    # This is the expected format for userTime
    stringFormat = r'^\d{2}:\d{2}:\d{2}$'

    # match() determines if the userTime is in the same format as the stringFormat
    if not re.match(stringFormat, userTime):
        print(
            "Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time\n")

    else:

        # userTime is split into hours, minutes, seconds using the colons as delimiters
        hours, minutes, seconds = map(int, userTime.split(':'))
        # The user entered time (now split and stored) are converted to a timedelta datetime type and stored
        userDeltaTime = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

        # Compares the user entered time to the timeDelivered attribute of the specified package
        # If user inputs a time after the time the package was delivered, program outputs "Delivered" and the time of delivery
        if userDeltaTime >= package.timeDelivered:
            print("Package ID: " + str(package.ID))
            print("Address: " + str(package.address))
            print("Deadline: " + str(package.deliveryDeadline))
            print("City: " + str(package.city))
            print("Zip: " + str(package.zip))
            print("Weight: " + str(package.weight) + " KG")
            print("Delivered at " + str(package.timeDelivered))

        # If the package has not been delivered yet, the findTruck function helps determine the start time of the truck the package is on
        # If userTime is after the start time of the truck the package is on, then the package's status is "En Route".
        # Otherwise, package status is "at the hub"
        elif userDeltaTime < package.timeDelivered:
            truck = findTruck(pID, trucks)
            if truck.startTime <= userDeltaTime:
                print("Package ID: " + str(package.ID))
                print("Address: " + str(package.address))
                print("Deadline: " + str(package.deliveryDeadline))
                print("City: " + str(package.city))
                print("Zip: " + str(package.zip))
                print("Weight: " + str(package.weight) + " KG")
                print("En route. To be delivered at: " + str(package.timeDelivered))

            else:
                print("Package ID: " + str(package.ID))
                print("Address: " + str(package.address))
                print("Deadline: " + str(package.deliveryDeadline))
                print("City: " + str(package.city))
                print("Zip: " + str(package.zip))
                print("Weight: " + str(package.weight) + " KG")
                print("At the hub. To be delivered at: " + str(package.timeDelivered))


# This function looks up all packages by their ID and returns all details including the delivery status,
# which is based on the user entered time
# O(n) time complexity
# O(1) space complexity
def lookupAllPackages(pID, userTime):
    package = packageHash.lookUp(pID)

    # Compares the user entered time to the timeDelivered attribute of the specified package
    # If user inputs a time after the time the package was delivered, program outputs "Delivered" and the time of delivery
    if userTime >= package.timeDelivered:
        print("Package ID: " + str(package.ID))
        print("Address: " + str(package.address))
        print("Deadline: " + str(package.deliveryDeadline))
        print("City: " + str(package.city))
        print("Zip: " + str(package.zip))
        print("Weight: " + str(package.weight) + " KG")
        print("Delivered at " + str(package.timeDelivered))
        print("\n")

        # If the package has not been delivered yet, the findTruck function helps determine the start time of the truck the package is on
        # If userTime is after the start time of the truck the package is on, then the package's status is "En Route".
        # Otherwise, package status is "at the hub"
    elif userTime < package.timeDelivered:
        truck = findTruck(pID, trucks)
        if truck.startTime <= userTime:
            print("Package ID: " + str(package.ID))
            print("Address: " + str(package.address))
            print("Deadline: " + str(package.deliveryDeadline))
            print("City: " + str(package.city))
            print("Zip: " + str(package.zip))
            print("Weight: " + str(package.weight) + " KG")
            print("En route. To be delivered at: " + str(package.timeDelivered))
            print("\n")

        else:
            print("Package ID: " + str(package.ID))
            print("Address: " + str(package.address))
            print("Deadline: " + str(package.deliveryDeadline))
            print("City: " + str(package.city))
            print("Zip: " + str(package.zip))
            print("Weight: " + str(package.weight) + " KG")
            print("At the hub. To be delivered at: " + str(package.timeDelivered))
            print("\n")


# This class will contain the command line interface
# The user will be prompted to choose between seeing the delivery status of a package, seeing the total mileage of all the trucks, or exiting the program
class main:

    # while True causes program to loop
    # If an unexpected input occurs, a line is printed (stating an incorrect input occurred), and the program will be restarted
    while True:
        userInput = input(
            "Welcome to the WGUPS application:\nTo lookup individual package details, press 1\nFor details about every package, press 2"
            "\nFor total mileage of all 3 trucks, press 3\nTo check the total time for all trucks, press 4\nTo check status of all packages, press 5\nTo exit, press 6")

        # User selected 1
        if userInput == "1":

            # User inputs packageID
            userPackID = int(float(input("Please provide your package ID: ")))

            # Determines the packageID is valid, then searches packageHash for the ID
            if(userPackID > 0) and (userPackID <= 40):
                lookup(userPackID)
            else:
                print("Not a valid package ID, please choose a number between 1 and 40\n")

        elif userInput == '2':
            userTime = input("Please provide the time in which you are interested in using military time (24-hour clock) and the format HH:MM:SS: ")

            # This is the expected format for userTime
            stringFormat = r'^\d{2}:\d{2}:\d{2}$'

            # match() determines if the userTime is in the same format as the stringFormat
            if not re.match(stringFormat, userTime):
                print(
                    "Incorrect format. Please format the time at which you are interested correctly: HH:MM:SS, including the colons, in 24-Hour time\n")
            else:
                # userTime is split into hours, minutes, seconds using the colons as delimiters
                hours, minutes, seconds = map(int, userTime.split(':'))
                # The user entered time (now split and stored) are converted to a timedelta datetime type and stored
                userDeltaTime = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

                for truck in trucks:
                    for packageID in truck.packages:
                        lookupAllPackages(packageID, userDeltaTime)

        # User selected 3
        # This is the sum of the milesTravelled of all 3 trucks
        elif userInput == "3":
            print("The total mileage of the 3 trucks combined is " + str(
                t1.milesTravelled + t2.milesTravelled + t3.milesTravelled) + " miles.")
            print("Truck 1: " + str(t1.milesTravelled))
            print("Truck 2: " + str(t2.milesTravelled))
            print("Truck 3: " + str(t3.milesTravelled))

        # User selected 4
        # Shows total time to deliver all packages for each truck
        elif userInput == "4":
            print("Truck 1: " + str(t1.totalTime))
            print("Truck 2: " + str(t2.totalTime))
            print("Truck 3: " + str(t3.totalTime))

        # User selected 5
        # Returns delivery status of every package at specified time
        elif userInput == '5':
            allPackageStatus()

        # User selected 6.
        # Print statement and exit
        elif userInput == '6':
            print("Program exited, goodbye")
            exit()
        else:
            userInput = input(
                "Incorrect input, please select either a '1', '2','3', '4', or '5'. Press Enter to return to the program\n")