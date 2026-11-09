from datetime import datetime, timezone

class Cab:
    def __init__(self,driver,seats,destination,pickup_time,passengers,has_left = False):
        self.driver = driver
        self.seats = seats
        self.destination = destination  
        self.pickup_time = pickup_time
        self.has_left = has_left
        self.passengers = passengers if passengers is not None else []

    def __str__(self):
        return f'Cab_Detail\nDriver:{self.driver}, Destination:{self.destination} , Pickup:{self.pickup_time}'


class RideRequests:
    def __init__(self,name,destination,pickup_time,year,sequence,status,req_time=None):
        self.name = name
        self.destination = destination
        self.pickup_time = pickup_time
        self.year = year
        self.sequence = sequence
        self.status = status
        self.req_time = req_time if req_time is not None else datetime.now(timezone.utc)

    def __str__(self):
        return f'Ride Detail\nName:{self.name} , Destination:{self.destination} , Pickup:{self.pickup_time}'