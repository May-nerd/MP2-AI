from problem import maxone,knapsack,vertex_cover

from solver.ga import GeneticSolver
from fn.ga import *
from fn.fitness import *
from utils import *

def select_problem(problem_name,config):
    if problem_name == 'maxone':
        problem = maxone.problem(16)
        config.fitness_fn = maxone_fitness
        config.feasibility_minimum = 0
        config.best_possible_score = problem.N
    elif problem_name == 'knapsack':
        problem = knapsack.problem(99)
        config.fitness_fn = knapsack_fitness
        config.feasibility_minimum = 100
        config.best_possible_score = problem.total_value
    elif problem_name == 'vertex_cover':
        problem = vertex_cover.problem(99)
        config.fitness_fn = vertex_cover_fitness
        config.feasibility_minimum = 100
        config.best_possible_score = len(problem.variables)

    return problem

def main():
    config = Config()

    # problem_name = 'maxone'
    problem_name = 'knapsack'
    # problem_name = 'vertex_cover'

    problem = select_problem(problem_name,config)
    config.best_possible_score += config.feasibility_minimum
    config.initial_solution = 'random'
    config.max_parent_try = 500
    config.max_iterations =  200
    config.max_flat_iterations = 50
    config.random_seed =   123456789
    config.explain = True

    # POPULATION
    config.population_size = 20     # 20, 50
    config.replace_population = generational
    # config.replace_population = choose_best

    # SELECTION
    config.max_parent_similarity = 0.9 # 0.9, 0.5
    config.select_parents = fitness_proportionate
    # config.select_parents = tournament_selection
    config.tournament_k = int(0.2 * config.population_size)

    # CROSSOVER
    config.prob_crossover = 0.90    # 0.90, 0.60
    config.crossover = one_point_crossover
    # config.crossover = two_point_crossover
    # config.crossover = uniform_crossover

    # MUTATION
    config.prob_mutate =  0.5   # 0.3, 0.5
    config.mutate =  change_one_value
    # config.mutate =  change_k_values(2)
    # config.mutate =  swap_two_values


    solver = GeneticSolver(problem,config)
    solver.solve()
    display_solutions(problem,solver)


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    end = time.time()
    elapsed = end - start
    print('Time elapsed: %ds' % elapsed)

