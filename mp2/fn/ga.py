import random

### STATISTICS ####
def create_cdf(pdf):
	return [(i,sum(p for j,p in pdf if j <= i)) for i,_ in pdf]

def random_selection(cdf):
	return [i for i,p in cdf if random.random() < p][0]


### SOLUTION SIMILARITY ###
def compute_similarity(state1,state2):
	solution1 = repr(state1)
	solution2 = repr(state2)
	count = 0.0
	for i in range(len(solution1)):
		s1 = solution1[i]
		s2 = solution2[i]
		if s1 == s2:
			count += 1
	return count / len(solution1)

### SELECTION FUNCTIONS ###

def fitness_proportionate(population,config):
	# Compute the probability distribution, based on fitness scores
	pdf = []
	total_score = 1.0 * sum([state.score for state in population])
	for i,state in enumerate(population):
		probability = state.score / total_score
		pdf.append((i,probability))
		if config.explain: print('\t',i,repr(state),'%.4f' % probability)
	cdf = create_cdf(pdf)
	
	# Select parents
	parents = []
	num_pairs = len(population) / 2
	iteration = 0
	while len(parents) != num_pairs:
		iteration += 1
		if iteration == config.max_parent_try:
			return [] # no parents
			
		index1 = random_selection(cdf)
		index2 = random_selection(cdf)

		if config.explain: print('\t Pair #%d' % len(parents))

		parent1 = population[index1]
		parent2 = population[index2]
		if config.explain: print('\t\t Parent1',parent1)
		if config.explain: print('\t\t Parent2',parent2)

		if (parent1,parent2) in parents:
			if config.explain: print('\t\t Already Exists')
			continue # dont add existing pairs

		similarity = compute_similarity(parent1,parent2)
		if config.explain: print('\t\t Similarity',similarity)
		if similarity <= config.max_parent_similarity:
			parents.append((parent1,parent2))


	return parents

def tournament_selection(population,config):
	parents = []
	num_pairs = len(population) / 2
	iteration = 0
	while len(parents) != num_pairs:
		if config.explain: print('\t Pair #%d' % len(parents))
		iteration += 1
		if iteration == config.max_parent_try:
			return [] # no parents

		pair = []
		for i in range(2): # 2 parents
			choices = []
			# Select k at random
			for k in range(config.tournament_k):
				choices.append(random.choice(population))
			best_choice = max(choices,key=lambda state: state.score)
			pair.append(best_choice)
			if config.explain: print('\t\tChoices',choices)
			if config.explain: print('\t\tParent%d' % (i+1),best_choice)

		parent1,parent2 = pair
		if (parent1,parent2) in parents:
			if config.explain: print('\t\t Already Exists')
			continue # dont add existing pairs

		similarity = compute_similarity(parent1,parent2)
		if config.explain: print('\t\t Similarity',similarity)
		if similarity <= config.max_parent_similarity:
			parents.append((parent1,parent2))

			
	return parents

### CROSSOVER FUNCTIONS ###

def one_point_crossover(parent1,parent2,prob_crossover):
	parent1_vector = parent1.vector 
	parent2_vector = parent2.vector
	vector_length = len(parent1_vector)

	# Randomize crossover point, from 25% - 75%
	min_index = int(vector_length * 0.25)
	max_index = int(vector_length * 0.75)
	crossover_index = random.choice(range(min_index,max_index+1))

	if random.random() < prob_crossover:
		child1_vector = parent1_vector[:crossover_index] + parent2_vector[crossover_index:]
		child2_vector = parent2_vector[:crossover_index] + parent1_vector[crossover_index:]
	else:
		child1_vector = parent1_vector
		child2_vector = parent2_vector

	child1 = parent1.copy()
	child2 = parent2.copy()
	child1.update_solution(child1_vector)
	child2.update_solution(child2_vector)
	return child1,child2

def two_point_crossover(parent1,parent2,prob_crossover):
	parent1_vector = parent1.vector 
	parent2_vector = parent2.vector
	vector_length = len(parent1_vector)

	# Fixed crossover indices: 1/3 and 2/3
	index1 = int(vector_length * 0.33)
	index2 = int(vector_length * 0.67)

	if random.random() < prob_crossover:
		child1_vector = parent1_vector[:index1] + parent2_vector[index1:index2] + parent1_vector[index2:]
		child2_vector = parent2_vector[:index1] + parent1_vector[index1:index2] + parent2_vector[index2:]
	else:
		child1_vector = parent1_vector
		child2_vector = parent2_vector

	child1 = parent1.copy()
	child2 = parent2.copy()
	child1.update_solution(child1_vector)
	child2.update_solution(child2_vector)
	return child1,child2

def uniform_crossover(parent1,parent2,prob_crossover):
	parent1_vector = parent1.vector
	parent2_vector = parent2.vector
	vector_length = len(parent1_vector)

	child1_vector = []
	child2_vector = []
	for i in range(vector_length):
		if random.random() < prob_crossover:
			child1_vector.append(parent2_vector[i])
			child2_vector.append(parent1_vector[i])
		else:
			child1_vector.append(parent1_vector[i])
			child2_vector.append(parent2_vector[i])

	child1 = parent1.copy()
	child2 = parent2.copy()
	child1.update_solution(child1_vector)
	child2.update_solution(child2_vector)
	return child1,child2


### MUTATION FUNCTIONS ###

def change_one_value(state,prob_mutation):
	if random.random() < prob_mutation: 
		problem = state.problem
		solution = state.solution 

		var = random.choice(problem.variables)
		value = solution[var]
		while value == solution[var]: # make sure it's another value
			value = random.choice(problem.domain[var])

		new_state = state.copy()
		new_state.solution[var] = value

		return new_state
	else:
		return state

def change_k_values(k):
	def mutation_fn(state,prob_mutation):
		if random.random() < prob_mutation:
			problem = state.problem
			solution = state.solution 
			new_state = state.copy()

			for i in range(k):
				var = random.choice(problem.variables)
				value = solution[var]
				while value == solution[var]: # make sure it's another value
					value = random.choice(problem.domain[var])

				new_state.solution[var] = value
			return new_state
		else:
			return state

	return mutation_fn

def swap_two_values(state,prob_mutation):
	if random.random() < prob_mutation:
		problem = state.problem
		solution = state.solution 

		var1 = random.choice(problem.variables)
		var2 = var1
		while var2 == var1: # make sure it's another variable
			var2 = random.choice(problem.variables)

		value1 = solution[var1]
		value2 = solution[var2]

		new_state = state.copy()
		new_state.solution[var1] = value2
		new_state.solution[var2] = value1
		return new_state
	else:
		return state


### POPULATION REPLACEMENT FUNCTIONS ###

def generational(current_pop,new_pop):
	""" Replace current population with new population """
	return new_pop 

def choose_best(current_pop,new_pop):
	""" Choose best from the current + new population """
	population_size = len(current_pop)
	whole_pop = current_pop + new_pop
	sorted_pop = sorted(whole_pop,key=lambda state: state.score,reverse=True)
	best_pop = sorted_pop[:population_size]
	return best_pop

