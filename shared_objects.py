import math


class Load:
    def __init__(self, id, pickup, dropoff):
        self.id = id
        self.pickup = Location(pickup)
        self.dropoff = Location(dropoff)
        self.satisfied = False
        self.cost = Location.calculate_distance(from_loc=self.pickup,
                                                to_loc=self.dropoff)


class Location:
    def __init__(self, location_set):
        x, y = location_set
        self.x = x
        self.y = y

    @staticmethod
    def calculate_distance(from_loc, to_loc):
        return math.sqrt((to_loc.x - from_loc.x) ** 2 + (to_loc.y - from_loc.y) ** 2)


class Driver:
    def __init__(self, depot):
        self.remained_capacity = 12 * 60
        self.current_location = depot
        self.load_list = []
        self.total_path_cost = 0
        self.available = True


class Depot:
    def __init__(self, location_set):
        self.location = Location(location_set=location_set)
