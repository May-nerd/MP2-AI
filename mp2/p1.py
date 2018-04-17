from problem import plants,einstein
from problem import magic_square,magic_series
from problem import knapsack,vertex_cover

from solver.bf import BruteForceSolver
from solver.bt import BacktrackingSolver
from fn.bt import * 
from utils import * 


def test1():
    # problem_name = 'plants'
    problem_name = 'magic_square'
    # problem_name = 'magic_series'
    # problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    # solver_name = 'brute_force'
    solver_name = 'backtracking'

    # solution_limit = 0
    solution_limit = 1

    problem = select_problem(problem_name)

    config = Config()
    config.solution_limit = solution_limit
    config.max_iterations = 999999
    config.explain = False

    if solver_name == 'brute_force':
        config.all_different = problem_name in ['plants','magic_square'] # permutation for these problems
        solver = BruteForceSolver(problem,config)
    elif solver_name == 'backtracking':
        config.select_variable_fn = first_unassigned
        config.sort_values_fn = default_order
        config.filter_fn = do_nothing
        solver = BacktrackingSolver(problem,config)

    solver.solve()
    print('Solutions found:',len(solver.solutions))
    # display_solutions(problem,solver)
    print('%s \t %s \t limit = %d' % (problem_name,solver_name,solution_limit))

def test2():
    problem_name = 'plants'
    # problem_name = 'einstein'
    # problem_name = 'magic_square'
    # problem_name = 'magic_series'
    # problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    option = 'with_filtering'
    # option = 'no_filtering'

    solution_limit = 0
    # solution_limit = 1

    problem = select_problem(problem_name)

    config = Config()
    config.solution_limit = solution_limit
    config.max_iterations = 999999
    config.explain = False

    config.select_variable_fn = first_unassigned
    config.sort_values_fn = default_order

    if option == 'no_filtering':
        config.filter_fn = do_nothing
    elif option == 'with_filtering':
        config.filter_fn = forward_checking
    
    solver = BacktrackingSolver(problem,config)
    solver.solve()
    print('Solutions found:',len(solver.solutions))
    # display_solutions(problem,solver)
    print('%s \t %s \t limit = %d' % (problem_name,option,solution_limit))

def test3():
    # problem_name = 'plants'
    # problem_name = 'einstein'
    problem_name = 'magic_square'
    # problem_name = 'magic_series'
    # problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    solution_limit = 0
    # solution_limit = 1

    problem = select_problem(problem_name)

    config = Config()
    config.solution_limit = solution_limit
    config.max_iterations = 999999
    config.explain = False

    config.select_variable_fn = custom_variable_selector
    config.sort_values_fn = custom_value_ordering
    config.filter_fn = forward_checking
    

    solver = BacktrackingSolver(problem,config)
    solver.solve()
    print('Solutions found:',len(solver.solutions))
    # display_solutions(problem,solver)
    print('%s \t limit = %d' % (problem_name,solution_limit))


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
        problem = knapsack.problem(test_case=2)
    elif problem_name == 'vertex_cover':
        problem = vertex_cover.problem(test_case=4)
    return problem

if __name__ == '__main__':
    import time
    start = time.time()

    test = 1

    if test == 1:
        test1()
    elif test == 2:
        test2()
    elif test == 3:
        test3()

    end = time.time()
    elapsed = end - start
    print('Test %d, Time elapsed: %ds' % (test,elapsed))

