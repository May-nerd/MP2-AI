from problem import maxone,knapsack,vertex_cover

from solver.ls import StochasticLocalSearchSolver
from solver.sa import AnnealingSolver
from fn.ls import *
from fn.objective import *
from fn.custom import *
from utils import *

def common_config():
    config = Config()
    config.max_restarts = 5
    config.max_iterations = 200
    config.max_flat_iterations = 50
    config.max_neighbor_try = 100
    config.initial_solution = 'random'
    config.respawn_solution = 'random'
    config.comparison_option = 'no_degradation'
    config.random_seed = 123456789
    return config

def test1():
    config = common_config()
    problem = select_problem('maxone',config)

    generator_name = 'change2'
    # generator_name = 'swap2'

    if generator_name == 'change2':
        config.neighbor_generator = change_upto_two_values_generator
    elif generator_name == 'swap2':
        config.neighbor_generator = swap_two_values_generator

    solver = StochasticLocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)
    # See check/p3.1.txt for correct answer

def test2():
    # problem_name = 'knapsack'
    problem_name = 'vertex_cover'

    config = common_config()
    problem = select_problem(problem_name,config)

    if problem_name == 'knapsack':
        config.neighbor_generator = knapsack_neighbor_generator
    elif problem_name == 'vertex_cover':
        config.neighbor_generator = vertex_cover_neighbor_generator

    solver = StochasticLocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)
    # See check/p3.2.txt for example answer

def test3():
    # problem_name = 'maxone'
    # problem_name = 'knapsack'
    problem_name = 'vertex_cover'

    # generator_name = 'change1'
    # generator_name = 'change2'
    # generator_name = 'swap2'
    generator_name = 'custom'

    config = common_config()
    problem = select_problem(problem_name,config)

    if generator_name == 'change1':
        config.neighbor_generator = change_one_value_generator
    elif generator_name == 'change2':
        config.neighbor_generator = change_upto_two_values_generator
    elif generator_name == 'swap2':
        config.neighbor_generator = swap_two_values_generator
    elif generator_name == 'custom':
        if problem_name == 'maxone':
            config.neighbor_generator = maxone_neighbor_generator
        elif problem_name == 'knapsack':
            config.neighbor_generator = knapsack_neighbor_generator
        elif problem_name == 'vertex_cover':
            config.neighbor_generator = vertex_cover_neighbor_generator

    solver = StochasticLocalSearchSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)

def test4():
    problem_name,test_case = 'knapsack',99
    # problem_name,test_case = 'vertex_cover',99

    option = 'no_degradation'
    # option = 'always_improve'

    generator_name = 'change1'
    # generator_name = 'change2'
    # generator_name = 'swap2'
    # generator_name = 'custom'

    solver_name = 'stochastic'
    # solver_name = 'annealing'

    alpha = 0.50
    # alpha = 0.75
    # alpha = 0.95

    config = common_config()
    config.comparison_option = option
    problem = select_problem(problem_name,config,test_case)

    if generator_name == 'change1':
        config.neighbor_generator = change_one_value_generator
    elif generator_name == 'change2':
        config.neighbor_generator = change_upto_two_values_generator
    elif generator_name == 'swap2':
        config.neighbor_generator = swap_two_values_generator
    elif generator_name == 'custom':
        if problem_name == 'knapsack':
            config.neighbor_generator = knapsack_neighbor_generator
        elif problem_name == 'vertex_cover':
            config.neighbor_generator = vertex_cover_neighbor_generator

    if solver_name == 'stochastic':
        solver = StochasticLocalSearchSolver(problem,config)
    elif solver_name == 'annealing':
        config.max_temperature = 100
        config.alpha = alpha
        solver = AnnealingSolver(problem,config)

    solver.solve()
    display_solutions(problem,solver)

def select_problem(problem_name,config,case_number=None):
    if problem_name == 'maxone':
        problem = maxone.problem(N=16)
        config.objective_fn = maxone_objective
        config.best_fn = max
        config.best_possible_score = problem.N
        if config.comparison_option == 'no_degradation':
            config.compare_fn = greater_than_equal
        else: # always improve
            config.compare_fn = greater_than
    elif problem_name == 'knapsack':
        test_case = case_number if case_number is not None else 3
        problem = knapsack.problem(test_case=test_case)
        config.objective_fn = knapsack_objective
        config.best_fn = max
        config.best_possible_score = problem.total_value
        if config.comparison_option == 'no_degradation':
            config.compare_fn = greater_than_equal
        else: # always improve
            config.compare_fn = greater_than
    elif problem_name == 'vertex_cover':
        test_case = case_number if case_number is not None else 5
        problem = vertex_cover.problem(test_case=test_case)
        config.objective_fn = vertex_cover_objective
        config.best_fn = min
        config.best_possible_score = 0
        if config.comparison_option == 'no_degradation':
            config.compare_fn = less_than_equal
        else: # always improve
            config.compare_fn = less_than

    return problem

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

    end = time.time()
    elapsed = end - start
    print('Test %d, Time elapsed: %ds' % (test,elapsed))
