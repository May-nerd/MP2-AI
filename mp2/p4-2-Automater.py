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
    bestConfigScore = 0;
    bestConfigList = [];
    configIterations = 0;

    # LISTS
    populationSizeList = [20,50]
    populationModelList = [(generational, "generational"), (choose_best, "choose_best")]
    
    parentSimilarityList = [0.9, 0.5]
    parentSelectionList = [ (fitness_proportionate, "fitness_proportionate") , (tournament_selection, "tournament_selection")]


    crossoverProbabilityList = [0.90, 0.60]
    crossoverTypeList = [(one_point_crossover,"one_point_crossover"), (two_point_crossover,"two_point_crossover"), (uniform_crossover, "uniform_crossover")]

    mutationProbabilityList = [0.3, 0.5]


    changekval2 = change_k_values(2)
    mutationTypeList = [(change_one_value, "change_one_value"), (changekval2, "changekval2"), (swap_two_values, "swap_two_values")]
    
    for popSize in populationSizeList:
        for popModel in populationModelList:
            for parentSim in parentSimilarityList:
                for parentSel in parentSelectionList: 
                    for crossoverProb in crossoverProbabilityList:
                        for crossoverType in crossoverTypeList:
                            for mutationProb in mutationProbabilityList:
                                for mutationType in mutationTypeList:
                                    config = Config()

                                    # problem_name = 'maxone'
                                    # problem_name = 'knapsack'
                                    problem_name = 'vertex_cover'

                                    problem = select_problem(problem_name,config)
                                    config.best_possible_score += config.feasibility_minimum
                                    config.initial_solution = 'random'
                                    config.max_parent_try = 500
                                    config.max_iterations =  200
                                    config.max_flat_iterations = 50
                                    config.random_seed =   123456789
                                    config.explain = False


                                    configList = []
                                    ################## CONFIG CHANGES STARTS HERE ########################################
                                    
                                    # POPULATION SIZE
                                    config.population_size = popSize     # 20, 50
                                    configList.append(("popSize", popSize))


                                    # POPULATION MODEL
                                    config.replace_population = popModel[0]
                                    # config.replace_population = choose_best
                                    configList.append(("popModel", popModel[1]))
                                    

                                    # SELECTION (PARENT SIMILARITY)
                                    config.max_parent_similarity = parentSim # 0.9, 0.5
                                    configList.append(("parentSim", parentSim))
                                    
                                    # SELECTION (PARENT SELECTION)
                                    config.select_parents = parentSel[0]
                                    # config.select_parents = tournament_selection
                                    configList.append(("parentSel", parentSel[1]))

                                    # TOURNAMENT (NO CHANGE)
                                    config.tournament_k = int(0.2 * config.population_size)


                                    # CROSSOVER PROBABILITY
                                    config.prob_crossover = crossoverProb   # 0.90, 0.60
                                    configList.append(("crossoverProb", crossoverProb))

                                    # CROSSOVER TYPE
                                    config.crossover = crossoverType[0]
                                    # config.crossover = two_point_crossover
                                    # config.crossover =" uniform_crossover
                                    configList.append(("crossoverType", crossoverType[1]))


                                    # MUTATION PROBABILITY
                                    config.prob_mutate =  mutationProb   # 0.3, 0.5
                                    configList.append(("mutationProb", mutationProb))

                                    # MUTATION TYPE
                                    config.mutate =  mutationType[0]
                                    # config.mutate =  change_k_values(2)
                                    # config.mutate =  swap_two_values
                                    configList.append(("mutationType", mutationType[1]))

                                    ################## CONFIG CHANGES ENDS HERE ########################################
                                    

                                    print("\n\nSOLVING: ")
                                    for item in configList:
                                        print(str(item[0]) + ": " + str(item[1]))


                                    solver = GeneticSolver(problem,config)
                                    solver.solve()

                                    #Get max config
                                    currentConfigScore = solver.getBestScore()
                                    print("SCORE: " + str(currentConfigScore))

                                    if(currentConfigScore > bestConfigScore):
                                        bestConfigScore = currentConfigScore
                                        bestConfigList = configList


                                    configIterations+=1


    print("\n\n\n\n\nTESTS DONE!" + problem_name)
    print("CONFIGS TESTED: " + str(configIterations))
    print("BEST CONFIGURATION SCORE: " + str(bestConfigScore))
    for item in bestConfigList:
        print(str(item[0]) + ": " + str(item[1]))


if __name__ == '__main__':
    import time
    start = time.time()

    main()

    end = time.time()
    elapsed = end - start
    print('Time elapsed: %ds' % elapsed)

