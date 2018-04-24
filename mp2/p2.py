from problem import plants,einstein
from problem import magic_square,magic_series
from problem import knapsack,vertex_cover

from solver.ls import LocalSearchSolver
from solver.tabu import TabuSolver
from fn.ls import *
from fn.objective import *
from utils import *

def common_config():
    config = Config()
    config.max_restarts = 20
    config.max_iterations = 100
    config.max_flat_iterations = 30
    config.random_seed = 123456789
    return config

def test1():
    problem = plants.problem()
    config = common_config()

    neighborhood_name = 'change2'
    # neighborhood_name = 'swap2'

    if neighborhood_name == 'change2':
        config.neighborhood_fn = change_upto_two_values
    elif neighborhood_name == 'swap2':
        config.neighborhood_fn = swap_two_values

    reverse = True # downhill
    hill_climbing_config(config,reverse)

    config.objective_fn = count_violations
    config.best_fn = min
    config.best_possible_score = 0

    config.initial_solution = 'random_permutation'
    config.respawn_solution = 'random_permutation'

    solver = LocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)
    # See check/p2.1.txt for correct answer

def test2():
    problem_name = 'plants'
    # problem_name = 'einstein'
    # problem_name = 'magic_square'
    # problem_name = 'magic_series'

    # neighborhood_name = 'change1'
    # neighborhood_name = 'change2'
    # neighborhood_name = 'swap2'
    # neighborhood_name = 'min_conflict'
    neighborhood_name = 'max_min_conflict'

    config = common_config()
    config.objective_fn = count_violations
    config.best_fn = min
    config.best_possible_score = 0
    config.initial_solution = 'random'
    config.respawn_solution = 'random'

    reverse = True # downhill
    if neighborhood_name == 'change1':
        config.neighborhood_fn = change_one_value
        hill_walking_config(config,reverse)
    elif neighborhood_name == 'change2':
        config.neighborhood_fn = change_upto_two_values
        hill_walking_config(config,reverse)
    elif neighborhood_name == 'swap2':
        config.neighborhood_fn = swap_two_values
        hill_walking_config(config,reverse)
    elif neighborhood_name == 'min_conflict':
        min_conflict_config(config)
    elif neighborhood_name == 'max_min_conflict':
        max_min_conflict_config(config)

    problem = select_problem(problem_name)
    solver = LocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)

def test3():
    problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    neighborhood_name = 'change1'
    # neighborhood_name = 'change2'
    # neighborhood_name = 'swap2'

    # see check/p2.3.txt to see results for change1

    problem = select_problem(problem_name)
    config = common_config()
    config.initial_solution = 'random'
    config.respawn_solution = 'random'

    if problem_name == 'knapsack':
        knapsack_config(config,problem)
        reverse = False # Uphill
    elif problem_name == 'vertex_cover':
        vertex_cover_config(config)
        reverse = True # downhill

    hill_climbing_config(config,reverse)
    if neighborhood_name == 'change1':
        config.neighborhood_fn = change_one_value
    elif neighborhood_name == 'change2':
        config.neighborhood_fn = change_upto_two_values
    elif neighborhood_name == 'swap2':
        config.neighborhood_fn = swap_two_values

    solver = LocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)

def test4():
    problem_name = 'plants'
    # problem_name = 'einstein'
    # problem_name = 'magic_square'
    # problem_name = 'magic_series'
    # problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    solver_name = 'hill_climb'
    # solver_name = 'hill_walk'
    # solver_name = 'random_walk'

    problem = select_problem(problem_name)
    config = common_config()
    config.initial_solution = 'random'
    config.respawn_solution = 'random'

    if problem_name in ['plants','einstein','magic_square','magic_series']:
        csp_config(config)
        config.neighborhood_fn = change_upto_two_values
        reverse = True # downhill
    elif problem_name == 'knapsack':
        knapsack_config(config,problem)
        config.neighborhood_fn = swap_two_values
        reverse = False # Uphill
    elif problem_name == 'vertex_cover':
        vertex_cover_config(config)
        config.neighborhood_fn = swap_two_values
        reverse = True # downhill

    if solver_name == 'hill_climb':
        hill_climbing_config(config,reverse)
    elif solver_name == 'hill_walk':
        hill_walking_config(config,reverse)
    elif solver_name == 'random_walk':
        random_walking_config(config,reverse)


    solver = LocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)

def test5():
    problem_name,test_case = 'knapsack',2
    # problem_name,test_case = 'knapsack',3
    # problem_name,test_case = 'vertex_cover',3
    # problem_name,test_case = 'vertex_cover',5

    tenure = 0
    # tenure = 3
    # tenure = 5
    # tenure = 7


    config = common_config()
    config.initial_solution = 'random'
    config.respawn_solution = 'random'
    config.neighborhood_fn = swap_two_values
    config.tabu_tenure = tenure

    if problem_name == 'knapsack':
        problem = knapsack.problem(test_case)
        knapsack_config(config,problem)
        config.selection_fn = select_max
        config.compare_fn = greater_than_equal
        config.aspiration = 50
    elif problem_name == 'vertex_cover':
        problem = vertex_cover.problem(test_case)
        vertex_cover_config(config)
        config.selection_fn = select_min
        config.compare_fn = less_than_equal
        config.aspiration = 5

    solver = TabuSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)

def select_problem(problem_name):
    if problem_name == 'plants':
        problem = plants.problem()
    elif problem_name == 'einstein':
        problem = einstein.problem()
    elif problem_name == 'magic_square':
        problem = magic_square.problem(N=3)
    elif problem_name == 'magic_series':
        problem = magic_series.problem(N=4)
    elif problem_name == 'knapsack':
        problem = knapsack.problem(test_case=3)
    elif problem_name == 'vertex_cover':
        problem = vertex_cover.problem(test_case=5)
    return problem

def hill_climbing_config(config,reverse):
    if reverse: # downhill
        config.legal_neighbor_fn = strictly_decreasing
        config.selection_fn = select_min
    else: # uphill
        config.legal_neighbor_fn = strictly_increasing
        config.selection_fn = select_max

def hill_walking_config(config,reverse):
    if reverse: # downhill
        config.legal_neighbor_fn = non_increasing
        config.selection_fn = select_min
    else: # uphill
        config.legal_neighbor_fn = non_decreasing
        config.selection_fn = select_max

def random_walking_config(config,reverse):
    # randomly select non-degrading neighbor, not best
    config.selection_fn = select_random
    if reverse: # downhill
        config.legal_neighbor_fn = non_increasing
    else: # uphill
        config.legal_neighbor_fn = non_decreasing

def min_conflict_config(config):
    config.neighborhood_fn = min_conflict
    config.legal_neighbor_fn = all_neighbors
    config.selection_fn = select_random

def max_min_conflict_config(config):
    config.neighborhood_fn = max_min_conflict
    config.legal_neighbor_fn = all_neighbors
    config.selection_fn = select_random

def csp_config(config):
    config.objective_fn = count_violations
    config.best_fn = min
    config.best_possible_score = 0

def knapsack_config(config,problem):
    config.objective_fn = knapsack_objective
    config.best_fn = max
    config.best_possible_score = problem.total_value

def vertex_cover_config(config):
    config.objective_fn = vertex_cover_objective
    config.best_fn = min
    config.best_possible_score = 0

if __name__ == '__main__':
    import time
    start = time.time()

    test = 3

    if test == 1:
        test1()
    elif test == 2:
        test2()
    elif test == 3:
        test3()
    elif test == 4:
        test4()
    elif test == 5:
        test5()

    end = time.time()
    elapsed = end - start
    print('Test %d, Time elapsed: %ds' % (test,elapsed))
