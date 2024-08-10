from shared_objects import Depot, Driver, Load, Location

import random


class StochasticGreedy:
    """this is a Greedy method + an initial guess of number of vehicles"""

    def __init__(self, loads):
        self.loads = loads
        self.satisfied_loads = []
        self.drivers = []
        self.depot = Depot((0, 0))
        self.available_drivers = 0

    def run(self):
        """"""
        result_paths = []
        driver_costs = []
        total_costs = 0
        '''_make_guess_on_required_vehicles'''
        potential_no_vehicles = self._make_guess_on_required_vehicles()
        self.available_drivers = potential_no_vehicles
        for i in range(potential_no_vehicles):
            self.drivers.append(Driver(self.depot.location))
        ''''''
        while len(self.satisfied_loads) != len(self.loads):
            '''check if we need a new driver'''
            if self.available_drivers == 0:
                self.drivers.append(Driver(self.depot.location))
                self.available_drivers += 1
            '''random driver'''
            d_ind = random.randint(0, len(self.drivers) - 1)
            # for d_ind in range(len(self.drivers)):
            self._find_and_go_to_lowest(d_ind)

        '''results'''
        for driver in self.drivers:
            result_paths.append(driver.load_list)
            driver_costs.append(driver.total_path_cost)
        return result_paths, driver_costs

    def _make_guess_on_required_vehicles(self):
        rough_cost = 0
        '''cost of all loads'''
        random_indices = [x for x in range(1, len(self.loads.values()) + 1)]
        random.shuffle(random_indices)
        '''randomly select two indices from the list. if two are not available, just consider one is depot'''
        current_loc = self.depot.location
        while len(random_indices) > 0:
            next_loc_indx = random_indices.pop(0)
            '''cost'''
            drv_to_pick = Location.calculate_distance(
                from_loc=current_loc,
                to_loc=self.loads[next_loc_indx].pickup)
            pick_to_drop = self.loads[next_loc_indx].cost
            rough_cost += drv_to_pick + pick_to_drop
            current_loc = self.loads[next_loc_indx].dropoff
        '''back to depot'''
        rough_cost += Location.calculate_distance(
            from_loc=current_loc,
            to_loc=self.depot.location)

        '''how many vehicle do we need?'''
        no_vehicles = int(rough_cost // Driver(self.depot.location).remained_capacity)
        return no_vehicles//3

    def _find_and_go_to_lowest(self, d_ind):
        if self.drivers[d_ind].available is False: return

        costs = []
        load_ids = []
        for load in self.loads.values():
            if load.satisfied: continue

            drv_to_pick = Location.calculate_distance(
                from_loc=self.drivers[d_ind].current_location,
                to_loc=load.pickup)
            pick_to_drop = load.cost
            drop_to_depot = Location.calculate_distance(
                from_loc=load.dropoff,
                to_loc=self.depot.location)
            if self.drivers[d_ind].remained_capacity > drv_to_pick + pick_to_drop + drop_to_depot:
                load_ids.append(load.id)
                costs.append(drv_to_pick + pick_to_drop)

        '''find min and go'''
        if len(costs) > 0:
            indx = costs.index(min(costs))
            load_id = load_ids[indx]
            self.drivers[d_ind].current_location = self.loads[load_id].dropoff
            self.drivers[d_ind].load_list.append(load_id)
            self.drivers[d_ind].total_path_cost += costs[indx]
            self.drivers[d_ind].remained_capacity -= costs[indx]

            self.satisfied_loads.append(load_id)
            self.loads[load_id].satisfied = True
        else:
            '''if no capacity, return '''
            drv_back_depot = Location.calculate_distance(
                from_loc=self.drivers[d_ind].current_location,
                to_loc=self.depot.location)

            self.drivers[d_ind].current_location = self.depot.location
            self.drivers[d_ind].total_path_cost += drv_back_depot
            self.drivers[d_ind].remained_capacity -= drv_back_depot
            self.drivers[d_ind].available = False

            self.available_drivers -= 1
