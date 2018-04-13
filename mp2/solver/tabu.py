from solver.ls import LocalSearchSolver, LocalSearchState

class TabuSolver(LocalSearchSolver):
	def local_search(self):
		config = self.config

		self.tabu_list = []

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

			# Neighbors
			neighbors = config.neighborhood_fn(state)
			print('\t %d neighbors' % len(neighbors))
			for neighbor in neighbors:
				neighbor.score = config.objective_fn(neighbor)
			neighbor_count += len(neighbors)

			# Legal neighbors: NOT TABU or REALLY GOOD
			legal_neighbors = []
			for neighbor in neighbors:
				if config.compare_fn(state,neighbor): # passes legal neighbor test
					if self.is_tabu(neighbor): # Check for exceptions
						# Neighbor is tabu, but has best possible score
						if neighbor.score == config.best_possible_score:
							legal_neighbors.append(neighbor)

						# Aspiration criteria: improvement >= aspiration
						improvement = abs(neighbor.score - state.score)
						if improvement >= config.aspiration:
							legal_neighbors.append(neighbor)
					else:
						legal_neighbors.append(neighbor)
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
			self.update_tabu_list(state)
			print('TABU LIST',self.tabu_list)

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

	def update_tabu_list(self,state):
		self.tabu_list.append(state.changes)
		if len(self.tabu_list) > self.config.tabu_tenure:
			self.tabu_list.pop(0) # remove oldest

	def is_tabu(self,state):
		changes = set(state.changes)
		for tabu_changes in self.tabu_list:
			tabu_changes = set(tabu_changes)
			common_changes = changes.intersection(tabu_changes)
			if len(common_changes) > 0:
				return True
		return False

