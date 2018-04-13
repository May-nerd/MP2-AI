class BacktrackingState:
	def __init__(self,problem,assignment):
		self.problem = problem
		self.assignment = assignment
		self.domain = {}

	def __repr__(self):
		return repr(self.assignment)

	@property 
	def solution(self):
		return dict(self.assignment)

	def assign(self,variable,value):
		self.assignment.append((variable,value))

	def copy(self):
		problem = self.problem
		assignment = self.assignment[:]
		clone = BacktrackingState(problem,assignment)
		clone.domain = {}
		for var,values in self.domain.items():
			clone.domain[var] = values[:]
		return clone

class BacktrackingSolver:
	def __init__(self,problem,config):
		self.problem = problem
		self.config = config
		self.solutions = []

	def solve(self):
		problem = self.problem
		config = self.config
		select_variable_fn = config.select_variable_fn
		sort_values_fn = config.sort_values_fn
		filter_fn = config.filter_fn

		self.process_domain_constraints()

		state = BacktrackingState(problem,assignment=[])
		state.domain = problem.domain

		stack = []
		stack.append(state)

		iteration = 1
		while True:
			if iteration > config.max_iterations:
				print('Iteration: %d -- LIMIT REACHED' % iteration)
				break

			if len(stack) == 0:
				print('Empty stack -- STOP')
				break

			if config.explain:
				print('*** STACK ***')
				for i,item in enumerate(reversed(stack)):
					print('\t',i,item)

			state = stack.pop()
			print(str(iteration).ljust(10),'TRY:',state)

			if self.is_complete(state.solution):
				print('Found solution at iteration %d: %s' % (iteration,str(state.solution)))
				self.solutions.append(state.solution)
				num_solutions = len(self.solutions)
				if num_solutions == config.solution_limit:
					print('Found %d solutions -- LIMIT REACHED' % num_solutions)
					break
				else:
					continue # skip the rest of loop: don't expand complete solution

			variable = select_variable_fn(state)
			sorted_values = sort_values_fn(state,variable)

			if len(sorted_values) == 0: # no possible values 
				print('No values for %s -- DEADEND' % str(variable))
				continue

			for value in reversed(sorted_values): # reverse for stack
				next_state = state.copy()
				next_state.assign(variable,value)
				filter_fn(next_state,variable)

				iteration += 1 # increase iteration count every time we do constraint check
				violation = problem.find_hard_violation(next_state.solution)
				if violation == None: # no violations, state can be extended
					stack.append(next_state)

				if config.explain: print('\t %s = %s' % (str(variable),str(value)),violation)

		print('Done after %d iterations' % iteration)

	def is_complete(self,solution):
		# Check if all variables are assigned a vallue in solution
		return set(self.problem.variables) == set(solution.keys())

	def process_domain_constraints(self):
		non_unary_constraints = []
		for constraint in self.problem.constraints:
			# Unary or Domain constraints
			if len(constraint.variables) == 1:
				variable = constraint.variables[0]
				valid_values = []
				for value in self.problem.domain[variable]:
					solution = {variable: value}
					pass_test = constraint.test(solution)
					if pass_test:
						valid_values.append(value)
				self.problem.domain[variable] = valid_values
			else:
				non_unary_constraints.append(constraint)

		self.problem.constraints = non_unary_constraints
