from parser import Parser
from greedy import Greedy
import argparse


def parse_data(path_to_problem: str):
    parser_obj = Parser(path_to_problem=path_to_problem)
    loads = parser_obj.parse()
    return loads


def greedy_alg(loads: [], dev=False):
    result_paths, driver_costs = Greedy(loads=loads).run()

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


if __name__ == "__main__":

    # path_to_problem = f'./Training _Problems/problem1.txt'
    '''arg parse'''
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_problem', type=str)
    args = parser.parse_args()
    path_to_problem = args.path_to_problem
    '''parse data'''
    loads = parse_data(path_to_problem)
    '''greedy'''
    greedy_alg(loads, dev=False)
