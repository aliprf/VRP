from shared_objects import Load


class Parser:
    def __init__(self, path_to_problem):
        self.path = path_to_problem

    def parse(self):
        """read problem file and extract loads"""
        loads = {}

        '''read'''
        with open(self.path, 'r') as file:
            lines = file.readlines()

            for i in range(1, len(lines)):
                load_number, pickup, dropoff = lines[i].strip().split()
                loads[int(load_number)] = Load(int(load_number), eval(pickup), eval(dropoff))
        return loads
