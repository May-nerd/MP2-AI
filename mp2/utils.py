class Config: pass

def display_solutions(problem,solver):
    print('%d solutions found' % len(solver.solutions))
    for solution in solver.solutions:
        print(problem.solution_format(problem,solution))
        print('*****' * 20)