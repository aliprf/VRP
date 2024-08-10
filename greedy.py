from shared_objects import Depot, Driver, Load, Location


class Greedy:
    def __init__(self, loads):
        self.loads = loads
        self.satisfied_loads = []
        self.drivers = []
        self.depot = Depot((0,0))


    def run(self):
        """"""
        result_paths = []
        driver_costs = []
        total_costs = 0
        ''''''
        while len(self.satisfied_loads) != len(self.loads):
            '''find possible candidate drivers'''
            driver, load_id, load_cost = self._find_candidate_driver()
            '''check if we need a new driver'''
            if driver is None:
                self.drivers.append(Driver(self.depot.location))
                continue
            '''perform the action'''
            driver.remained_capacity -= load_cost
            driver.current_location = self.loads[load_id].dropoff
            driver.total_path_cost += load_cost
            driver.load_list.append(load_id)
            ''''''
            self.satisfied_loads.append(load_id)
            self.loads[load_id].satisfied = True
        ''' dont forget that all drivers should go back to depot'''
        for driver in self.drivers:
            return_cost = Location.calculate_distance(
                from_loc=driver.current_location,
                to_loc=self.depot.location
            )
            driver.remained_capacity -= return_cost
            driver.current_location = self.depot.location
            driver.total_path_cost += return_cost
            '''results'''
            result_paths.append(driver.load_list)
            driver_costs.append(driver.total_path_cost)
        return result_paths, driver_costs
    def _find_candidate_driver(self):
        candidate_drivers = []
        load_ids = []
        costs = []
        for drv in self.drivers:
            load_id, load_cost = self._find_next_lowest(drv)
            if load_id is not None:
                candidate_drivers.append(drv)
                load_ids.append(load_id)
                costs.append(load_cost)

        if len(candidate_drivers) > 0:
            indx = costs.index(min(costs))
            return candidate_drivers[indx], load_ids[indx], costs[indx]
        else:
            return None, None, None
    def _find_next_lowest(self, driver):
        costs = []
        load_ids =[]
        for load in self.loads.values():
            if load.satisfied: continue

            drv_to_pick = Location.calculate_distance(
                from_loc=driver.current_location,
                to_loc=load.pickup)
            pick_to_drop = load.cost
            drop_to_depot = Location.calculate_distance(
                from_loc=load.dropoff,
                to_loc=self.depot.location)
            if driver.remained_capacity > drv_to_pick + pick_to_drop+drop_to_depot:
                load_ids.append(load.id)
                costs.append(drv_to_pick+pick_to_drop)
        '''return min'''
        if len(costs)>0:
            indx = costs.index(min(costs))
            return load_ids[indx], costs[indx]
        else:
            return None, None

