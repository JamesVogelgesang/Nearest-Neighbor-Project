# Creates Truck class with its own attributes
class Truck:
    def __init__(self, capacity, speed, startTime, milesTravelled, packages, currentAddress, totalTime):
        self.capacity = capacity
        self.speed = speed
        self.startTime = startTime
        self.milesTravelled = milesTravelled
        self.packages = packages
        self.currentAddress = currentAddress
        self.totalTime = totalTime

    # Prevents an object reference when print(Truck) is used
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (
            self.capacity, self.speed, self.startTime, self.milesTravelled, self.packages, self.currentAddress, self.totalTime)
