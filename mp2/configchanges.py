    # POPULATION SIZE
    config.population_size = 20     # 20, 50
    
    # POPULATION MODEL
    config.replace_population = generational
    # config.replace_population = choose_best

    # SELECTION (PARENT SIMILARITY)
    config.max_parent_similarity = 0.9 # 0.9, 0.5
    
    
    # SELECTION (PARENT SELECTION)
    config.select_parents = fitness_proportionate
    # config.select_parents = tournament_selection

    # TOURNAMENT (NO CHANGE)
    config.tournament_k = int(0.2 * config.population_size)


    # CROSSOVER PROBABILITY
    config.prob_crossover = 0.90    # 0.90, 0.60


    # CROSSOVER TYPE
    config.crossover = one_point_crossover
    # config.crossover = two_point_crossover
    # config.crossover = uniform_crossover


    # MUTATION PROBABILITY
    config.prob_mutate =  0.5   # 0.3, 0.5


    # MUTATION TYPE
    config.mutate =  change_one_value
    # config.mutate =  change_k_values(2)
    # config.mutate =  swap_two_values