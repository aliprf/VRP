import os

from parser import Parser
from greedy import Greedy
from improved_clustering import ImprovedCluster
import argparse
import sys


def parse_data(path_to_problem: str):
    parser_obj = Parser(path_to_problem=path_to_problem)
    loads = parser_obj.parse()
    return loads


def imp_cluster(loads: [], dev=False):
    result_paths, driver_costs = ImprovedCluster(loads=loads).run()
    total_cost = 0
    if dev:
        print('imp_cluster => ')
        print('total_costs')
        sum_dr_costs = 0
        for dc in driver_costs: sum_dr_costs += dc
        total_cost = len(result_paths) * 500 + sum_dr_costs
        print(total_cost)
        print('driver_costs')
        print(driver_costs)
        print('result_paths')
        print(result_paths)
        print('--------------------')
    else:
        for dr_path in result_paths:
            print(dr_path)

    return total_cost


def greedy_alg(loads: [], dev=False):
    result_paths, driver_costs = Greedy(loads=loads).run()
    total_cost = 0
    if dev:
        print('greedy_alg => ')
        print('total_costs')
        sum_dr_costs= 0
        for dc in driver_costs: sum_dr_costs+= dc
        total_cost = len(result_paths) * 500 + sum_dr_costs
        print(total_cost)
        print('driver_costs')
        print(driver_costs)
        print('result_paths')
        print(result_paths)
        print('--------------------')
    else:
        for dr_path in result_paths: print(dr_path)

    return total_cost


if __name__ == "__main__":
    # path_to_problem = f'./Training_Problems/problem18.txt'
    # imp_cluster(loads=parse_data(path_to_problem), dev=True)
    # greedy_alg(loads=parse_data(path_to_problem), dev=True)

    dev = False
    if dev:
        total_cost =0
        prefix = f'./Training_Problems/'
        problems_paths = os.listdir(prefix)
        for ptp in problems_paths:
            pp = os.path.join(prefix, ptp)
            total_cost += imp_cluster(parse_data(pp), dev=False)
        # print(total_cost/len(problems_paths))
    else:
        '''arg parse'''
        path_to_problem = sys.argv[1]

        # parser = argparse.ArgumentParser()
        # parser.add_argument("--path_to_problem", required=True, help="Path to the problem file")
        # args = parser.parse_args()
        # pp = args.path_to_problem
        '''parse data'''
        loads = parse_data(path_to_problem=path_to_problem)
        '''greedy'''
        imp_cluster(loads, dev=False)
