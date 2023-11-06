# Creates the packages class with the listed attributes
class Package:
    def __init__(self, ID, address, city, state, zip, deliveryDeadline, weight, status):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryDeadline = deliveryDeadline
        self.weight = weight
        self.status = status
        self.timeDelivered = None

    # Prevents object reference when print(Package) is used
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.ID, self.address, self.city, self.state, self.zip, self.deliveryDeadline, self.weight, self.status)


