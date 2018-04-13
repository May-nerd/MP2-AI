import random

class GeneticState:
	def __init__(self,problem,solution):
		self.problem = problem
		self.solution = solution 
		self.score = None

	def __repr__(self):
		string_values = [str(self.solution[var]) for var in self.problem.variables]
		return ''.join(string_values)

	def copy(self):
		problem = self.problem
		solution = self.solution.copy()
		clone = GeneticState(problem,solution)
		return clone 

	@property
	def vector(self):
		vector = [self.solution[var] for var in self.problem.variables]
		return vector

	def update_solution(self,vector):
		solution = {}
		for i,var in enumerate(self.problem.variables):
			solution[var] = vector[i]
		self.solution = solution

class GeneticSolver:
	def __init__(self,problem,config):
		self.problem = problem
		self.config = config
		self.solutions = []

	def generate_random_solution(self):
		solution = {}
		for var in self.problem.variables:
			solution[var] = random.choice(self.problem.domain[var])
		return solution

	def generate_random_permutation(self):
		# assume all vars have same domain
		variables = self.problem.variables
		var = variables[0]
		values = self.problem.domain[var][:]
		random.shuffle(values)

		return dict(zip(variables,values))

	def solve(self):
		config = self.config

		if config.random_seed is not None:
			random.seed(config.random_seed)

		best_per_generation = []

		population = self.initialize_population()
		best_solution = max(population, key=get_score)
		best_per_generation.append(best_solution)

		iteration = 1
		flat_count = 0
		while True:
			if iteration > config.max_iterations:
				if config.explain: print('Iteration: %d -- LIMIT REACHED' % iteration)
				break

			if config.explain: 
				print('Iteration %d' % iteration)
				for i,state in enumerate(population):
					print('\t',i,repr(state),state.score)

			# Select parents
			if config.explain: print('SELECTION')
			parents = config.select_parents(population,config)
			
			if len(parents) == 0:
				pair_count = len(population) / 2
				if config.explain: print('Not able to select %d pairs of parents -- solutions in population too similar' % pair_count)
				break

			# Create children
			children = []
			if config.explain: print('CREATING CHILDREN')
			for parent1,parent2 in parents:
				if config.explain: print('\tParents',repr(parent1),repr(parent2))

				child1,child2 = config.crossover(parent1,parent2,config.prob_crossover)
				if config.explain: print('\t\tCrossover',repr(child1),repr(child2))

				child1 = config.mutate(child1,config.prob_mutate)
				child2 = config.mutate(child2,config.prob_mutate)
				if config.explain: print('\t\tMutation',repr(child1),repr(child2))

				child1.score = config.fitness_fn(child1,config.feasibility_minimum)
				child2.score = config.fitness_fn(child2,config.feasibility_minimum)

				children.append(child1)
				children.append(child2)


			best_solution = max(children, key=get_score)
			best_per_generation.append(best_solution)
			
			# Check if found best possible score
			if best_solution.score == config.best_possible_score:
				if config.explain: print('Found best possible solution:',state.solution)
				break

			# Detect no improvement of best solution
			prev_best, current_best = best_per_generation[-2], best_per_generation[-1]
			if current_best.score == prev_best.score:
				flat_count += 1
			else: # reset flat counter
				flat_count = 0

			if flat_count == config.max_flat_iterations:
				if config.explain: print('NO IMPROVEMENT FOR %d iterations -- STOP' % flat_count)
				break

			# Replace population
			population = config.replace_population(population,children)

			iteration += 1


		best_state = max(best_per_generation, key=get_score)
		if config.explain: print('Best score:', best_state.score)
		self.solutions = [best_state.solution]

		if config.explain: print('Iterations:',iteration)

		self.best_score = best_state.score
		self.iterations = iteration

	def initialize_population(self):
		if self.config.explain: print('Initializing population...')
		config = self.config

		solutions = []
		while len(solutions) != config.population_size:
			if config.initial_solution == 'random':
				solution = self.generate_random_solution()
			elif config.initial_solution == 'random_permutation':
				solution = self.generate_random_permutation()

			if solution not in solutions: # don't repeat solutions
				solutions.append(solution)

		population = []
		for solution in solutions:
			state = GeneticState(self.problem,solution)
			state.score = config.fitness_fn(state,config.feasibility_minimum)
			population.append(state)

		return population


def get_score(state):
	return state.score
