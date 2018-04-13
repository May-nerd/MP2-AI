from problem import plants, magic_square, magic_series
from problem import knapsack, vertex_cover

from solver.bf import BruteForceSolver
from utils import * 

def test1():
    problem = magic_square.problem(N=3)     # 3,4
    problem.display()
    # See check/p0.1.txt for correct answer

def test2():
    problem = magic_square.problem(N=3)
    problem.display()

    solver = brute_force_solver(problem)
    solver.config.all_different = True  # permutations only
    solver.solve()

    display_solutions(problem,solver)
    # See check/p0.2.txt for correct answer

def test3():
    problem = magic_series.problem(N=3) # 3,4,5,6
    problem.display()

    solver = brute_force_solver(problem)
    solver.config.all_different = False # all combinations
    solver.solve()

    display_solutions(problem,solver)
    # See check/p0.3.txt for correct answer

def test4():
    problem = knapsack.problem(test_case=0) # 0,1,2,3
    problem.display()

    solver = brute_force_solver(problem)
    solver.config.all_different = False # all combinations
    solver.solve()

    # Note: you might want to comment out display_solutions for test_case=2,3
    display_solutions(problem,solver)
    print('Solutions found:',len(solver.solutions))
    # See check/p0.4.txt for correct answer

def test5():
    problem = vertex_cover.problem(test_case=0) # 0,1,2,3,4,5
    problem.display()

    solver = brute_force_solver(problem)
    solver.config.all_different = False # all combinations
    solver.solve()

    # Note: uncomment display_solutions for test_case=3
    # display_solutions(problem,solver)
    print('Solutions found:',len(solver.solutions))
    # See checker/p0.5.txt for correct answer

def test6():
    problem_name = 'plants'     
    # problem_name = 'magic_square'
    option = 'combination'   
    # option = 'permutation'   

    if problem_name == 'plants':
        problem = plants.problem()
    elif problem_name == 'magic_square':
        problem = magic_square.problem(N=3)

    solver = brute_force_solver(problem)

    if option == 'combination':
        solver.config.all_different = False
    elif option == 'permutation':
        solver.config.all_different = True

    solver.solve()
    print('Solutions found:',len(solver.solutions))

def brute_force_solver(problem):
    config = Config()
    config.solution_limit = 0 # find all
    config.max_iterations = 9999999

    solver = BruteForceSolver(problem,config)
    return solver

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
    elif test == 4:
        test4()
    elif test == 5:
        test5()
    elif test == 6:
        test6()

    end = time.time()
    elapsed = end - start
    print('Test %d, Time elapsed: %ds' % (test,elapsed))
