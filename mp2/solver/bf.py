import itertools

class BruteForceSolver:
	def __init__(self,problem,config):
		self.problem = problem
		self.config = config 
		self.solutions = []

	def solve(self):
		variables = self.problem.variables
		domain = self.problem.domain 
		config = self.config

		if config.all_different:
			# all values must be different, use permutation
			# assume all variables have similar domains
			var = variables[0]
			values = domain[var] 
			value_combinations = itertools.permutations(values)
		else:
			# otherwise, use all possible combinations
			all_values = [domain[var] for var in variables]
			value_combinations = itertools.product(*all_values)

		print('Solving using Brute Force...')
		for i,values in enumerate(value_combinations):
			solution = dict(zip(variables,values))
			violation = self.problem.find_hard_violation(solution)

			print(str(i+1).ljust(10),values,violation)

			if violation is None:
				self.solutions.append(solution)
				num_solutions = len(self.solutions)
				if num_solutions == config.solution_limit:
					print('Found %d solutions -- LIMIT REACHED' % num_solutions)
					return

			if i == config.max_iterations:
				print('Iteration: %d -- LIMIT REACHED' % i)
				return 

