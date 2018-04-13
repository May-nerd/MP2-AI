from solver.ls import LocalSearchSolver, LocalSearchState
import random, math

class AnnealingSolver(LocalSearchSolver):
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
				
				neighbor_count += 1
				if config.compare_fn(state,neighbor):
					legal_neighbor = neighbor
					break
				else:
					temperature = self.compute_temperature(iteration)
					probability = self.compute_probability(state,neighbor,temperature)
					if probability > random.random():
						legal_neighbor = neighbor
						break

			if legal_neighbor is None:
				print('No legal neighbor found after %d tries -- LOCAL OPTIMUM FOUND' % config.max_neighbor_try)
				break
				
			legal_neighbor_count += 1

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
			if config.compare_fn(best_state,state): # compare current vs new
				best_state = state

			if state.score == config.best_possible_score:
				print('Found best possible solution:',state.solution)
				break

		self.last_state = best_state
		self.iterations = iteration
		self.neighbor_count = neighbor_count
		self.legal_neighbor_count = legal_neighbor_count

	def compute_temperature(self,iteration):
		config = self.config

		max_temperature = config.max_temperature
		alpha = config.alpha

		progress = math.ceil((iteration * 100) / config.max_iterations)
		return max_temperature * (alpha ** progress)

	def compute_probability(self,state,neighbor,temperature):
		score_diff = abs(state.score - neighbor.score)
		exponent = score_diff / temperature
		return math.exp(-exponent)
