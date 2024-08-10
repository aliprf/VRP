from shared_objects import Depot, Driver, Load, Location

import random


class RandomCluster:
    def __init__(self, loads):
        self.loads = loads
        self.satisfied_loads = set()
        self.drivers = []
        self.depot = Depot((0, 0))
        self.available_drivers = 0
        self.cost_map = None

    def run(self):
        result_paths = []
        driver_costs = []
        total_costs = 0

        self.cost_map = self._create_cost_map()
        self.drivers.append(Driver(self.depot.location))

        while len(self.satisfied_loads) != len(self.loads):
            add_new = True
            for i in self.loads.keys():
                load_id = self.loads[random.randint(1, len(self.loads))].id
                # load_id= i
                if load_id in self.satisfied_loads: continue
                if self._find_best_cluster(load_id): add_new = False
            if add_new:
                self.drivers.append(Driver(self.depot.location))

        '''results'''
        rem_ind =[]
        for i in range(len(self.drivers)):
            if len(self.drivers[i].load_list) ==0:
                rem_ind.append(i)
        self.drivers = [self.drivers[i] for i in range(len(self.drivers)) if i not in rem_ind]

        for driver in self.drivers:
            result_paths.append(driver.load_list)
            driver_costs.append(driver.total_path_cost)
        return result_paths, driver_costs

    def _find_best_cluster(self, load_id, max_capacity=12 * 60):
        driver_best_cluster_road = []
        driver_best_cluster_cost =[]
        driver_cost = {}
        for i in range(len(self.drivers)):
            if self.drivers[i].available is False: continue

            load_list, total_cost = self.find_best_insertion(load_id, i)
            if total_cost < max_capacity:
                driver_best_cluster_road.append(load_list)
                driver_best_cluster_cost.append(total_cost)
                driver_cost[total_cost] = i
            # else:
            #     driver_best_cluster_cost.append(total_cost)
            #     driver_best_cluster_road.append([])

        '''update lowest'''
        if len(driver_best_cluster_cost) ==0:
            return False
        load_list, total_cost= self._sort_by_max_length_and_cost(
            driver_best_cluster_road,
            driver_best_cluster_cost)

        indx = driver_cost[total_cost]
        ''''''
        self.drivers[indx].load_list = load_list
        self.drivers[indx].total_path_cost = total_cost
        self.drivers[indx].remained_capacity = max_capacity - total_cost
        for load_ids in load_list:
            self.satisfied_loads.add(load_ids)
            self.loads[load_ids].satisfied = True
        return True

    def _sort_by_max_length_and_cost(self, driver_best_cluster_road, driver_best_cluster_cost):
        combined = list(zip(driver_best_cluster_road, driver_best_cluster_cost))
        combined.sort(key=lambda x: (len(x[0]), x[1]))
        sorted_lists, sorted_costs = zip(*combined)
        sorted_lists = list(sorted_lists)
        sorted_costs = list(sorted_costs)
        return sorted_lists[-1], sorted_costs[-1]

    def find_best_insertion(self, load_id, d_indx):
        dr_load_list = self.drivers[d_indx].load_list.copy()
        sequences = []
        seq_cost = []
        length = len(dr_load_list)
        if length == 0:
            transitions = [f"{self.depot.id}->{load_id}",
                           f"{load_id}->{self.depot.id}"]
            sequences.append(transitions)
            seq_cost.append(self._calculate_pseq_cost(transitions))
        else:
            for i in range(length + 1):
                new_sequence = dr_load_list[:i] + [load_id] +dr_load_list[i:]
                transitions = [f"{self.depot.id}->{new_sequence[0]}"]
                transitions += [f"{new_sequence[j]}->{new_sequence[j + 1]}" for j in range(len(new_sequence) - 1)]
                transitions.append(f"{new_sequence[-1]}->{self.depot.id}")

                seq_cost.append(self._calculate_pseq_cost(transitions))
                sequences.append(transitions)

        '''find min cost of all possible sequence'''
        indx = seq_cost.index(min(seq_cost))
        ''' total cost of the drive after insertion: load cost + transition cost '''
        dr_load_list.insert(indx, load_id)
        total_cost = seq_cost[indx]+ self._calc_loads_cost(dr_load_list)
        '''check if it is below capacity'''

        return dr_load_list, total_cost

    def _calc_loads_cost(self, loads):
        cost = 0
        for id in loads:
            cost += self.loads[id].cost
        return cost

    def _calculate_pseq_cost(self, sequence):
        cost = 0
        for x in sequence:
            cost += self.cost_map[x]
        return cost

    def _create_cost_map(self):
        cmap = {}
        for i in self.loads.keys():
            for j in self.loads.keys():
                if i == j: continue
                cmap[str(self.loads[i].id) + '->' + str(self.loads[j].id)] = (
                        # self.loads[i].cost +
                        # self.loads[j].cost +
                        Location.calculate_distance(from_loc=self.loads[i].dropoff,
                                                    to_loc=self.loads[j].pickup)
                )
        '''depot'''
        for i in self.loads.keys():
            cmap[str(self.loads[i].id) + '->' + str(self.depot.id)] = (
                    # self.loads[i].cost +
                    Location.calculate_distance(from_loc=self.loads[i].dropoff,
                                                to_loc=self.depot.location)
            )
            cmap[str(self.depot.id) + '->' + str(self.loads[i].id)] = (
                    # self.loads[i].cost +
                    Location.calculate_distance(from_loc=self.depot.location,
                                                to_loc=self.loads[i].pickup)
            )

        return cmap
