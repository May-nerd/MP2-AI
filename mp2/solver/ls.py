import random

class LocalSearchState:
	def __init__(self,problem,solution):
		self.problem = problem
		self.solution = solution
		self.score = None

	def __repr__(self):
		return repr(self.solution)

	def copy(self):
		problem = self.problem
		solution = self.solution.copy()
		clone = LocalSearchState(problem,solution)
		return clone

class LocalSearchSolver:
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

		if config.initial_solution == 'random':
			self.config.initial_solution = self.generate_random_solution()
		elif config.initial_solution == 'random_permutation':
			self.config.initial_solution = self.generate_random_permutation()

		solutions = []
		restart = 0
		iterations = []
		neighbor_count = 0
		legal_neighbor_count = 0
		while True:
			print('Restart #%d' % restart)
			if restart == config.max_restarts:
				print('Restart limit reached')
				break

			self.local_search()

			state = self.last_state
			solutions.append(state)
			iterations.append(self.iterations)
			neighbor_count += self.neighbor_count
			legal_neighbor_count += self.legal_neighbor_count

			if state.score == config.best_possible_score:
				print('Found best possible solution:',state.solution)
				break

			if config.respawn_solution == 'last':
				self.config.initial_solution = self.last_state.solution
			elif config.respawn_solution == 'random':
				self.config.initial_solution = self.generate_random_solution()
			elif config.respawn_solution == 'random_permutation':
				self.config.initial_solution = self.generate_random_permutation()
			else:
				raise Exception('Invalid config.respawn_solution: %s' % config.respawn_solution)

			restart += 1

		best_state = config.best_fn(solutions,key=lambda state: state.score)
		print('Restarts:',len(iterations))
		print('Total iterations:',sum(iterations))
		print('Total neighbors:',neighbor_count)
		print('Total legal neighbors:',legal_neighbor_count)
		print('Best score:',best_state.score)
		self.solutions = [best_state.solution]

	def local_search(self):
		config = self.config

		solution = config.initial_solution
		state = LocalSearchState(self.problem,solution)
		state.score = config.objective_fn(state)

		iteration = 1
		flat_count = 0
		neighbor_count = 0
		legal_neighbor_count = 0
		while True:
			if iteration > config.max_iterations:
				print('Iteration: %d -- LIMIT REACHED' % iteration)
				break

			print(iteration,str(state.score).ljust(5),state.solution)

			# Neighbors
			neighbors = config.neighborhood_fn(state)
			print('\t %d neighbors' % len(neighbors))
			for neighbor in neighbors:
				neighbor.score = config.objective_fn(neighbor)
			neighbor_count += len(neighbors)

			# Legal Neighbors
			legal_neighbors = config.legal_neighbor_fn(state,neighbors)
			print('\t %d legal neighbors' % len(legal_neighbors))
			legal_neighbor_count += len(legal_neighbors)

			if len(legal_neighbors) == 0:
				print('No legal neighbors = LOCAL OPTIMUM FOUND -- STOP')
				break

			# Select legal neighbor
			neighbor = config.selection_fn(legal_neighbors)

			# Plateau detection: same score = flat
			if neighbor.score == state.score:
				flat_count += 1
			else: # reset flat counter
				flat_count = 0

			if flat_count == config.max_flat_iterations:
				print('STUCK ON PLATEAU FOR %d iterations -- STOP' % flat_count)
				break

			# Make neighbor the current solution
			state = neighbor
			iteration += 1

			if state.score == config.best_possible_score:
				print('Found best possible solution:',state.solution)
				break
				

		self.last_state = state
		self.iterations = iteration
		self.neighbor_count = neighbor_count
		self.legal_neighbor_count = legal_neighbor_count


class StochasticLocalSearchSolver(LocalSearchSolver):
	def local_search(self):
		config = self.config

		solution = config.initial_solution
		state = LocalSearchState(self.problem,solution)
		state.score = config.objective_fn(state)

		iteration = 1
		flat_count = 0
		neighbor_count = 0
		legal_neighbor_count = 0
		best_state = state
		while True:
			if iteration > config.max_iterations:
				print('Iteration: %d -- LIMIT REACHED' % iteration)
				break

			print(iteration,str(state.score).ljust(5),state.solution)

			legal_neighbor = None
			for i in range(config.max_neighbor_try):
				neighbor = next(config.neighbor_generator(state))
				neighbor.score = config.objective_fn(neighbor)
				if neighbor.solution == state.solution:
					continue # skip if same solution
				
				print('\t',i+1,str(neighbor.score).ljust(5),neighbor.solution)
				neighbor_count += 1
				if config.compare_fn(state,neighbor):
					legal_neighbor = neighbor
					legal_neighbor_count += 1
					break

			if legal_neighbor is None:
				print('No legal neighbor found after %d tries -- LOCAL OPTIMUM FOUND' % config.max_neighbor_try)
				break

			# Plateau detection: same score = flat
			if legal_neighbor.score == state.score:
				flat_count += 1
			else: # reset flat counter
				flat_count = 0

			if flat_count == config.max_flat_iterations:
				print('STUCK ON PLATEAU FOR %d iterations -- STOP' % flat_count)
				break

			# Make neighbor the current solution
			state = legal_neighbor

			iteration += 1

			# Check for best solution
			if config.compare_fn(best_state,state):
				best_state = state
				
			if state.score == config.best_possible_score:
				print('Found best possible solution:',state.solution)
				break
				

		self.last_state = best_state
		self.iterations = iteration
		self.neighbor_count = neighbor_count
		self.legal_neighbor_count = legal_neighbor_count
