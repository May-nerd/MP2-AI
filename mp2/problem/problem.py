class Problem:
	def __init__(self,variables,domain,constraints):
		self.variables = variables
		self.domain = domain
		self.constraints = constraints
		self.name = 'undefined'

	def __repr__(self):
		return 'Problem:%s' % self.name

	def display(self):
		print('*****' * 5)
		print(self)
		print('%d variables' % len(self.variables))
		for var in self.variables:
			print('\t',str(var).ljust(20),self.domain[var])
		print('%d constraints' % len(self.constraints))
		for constraint in self.constraints:
			print('\t',constraint)
			print('\t\t',constraint.variables)
		print('*****' * 5)

	def unassigned_variables(self,solution):
		unassigned_vars = []
		for variable in self.variables:
			if variable not in solution:
				unassigned_vars.append(variable)
		return unassigned_vars

	def find_hard_violation(self,solution):
		""" 
		Input: solution
		Output: a hard constraint violated by solution
		"""
		for constraint in self.constraints:
			if constraint.is_soft(): 
				continue # skip soft constraints

			pass_test = constraint.test(solution)
			if not pass_test:
				return constraint 
				
		return None # no violation found

	def all_hard_violations(self,solution,specific_variable=None):
		""" 
		Input: solution
		Output: list of hard constraints violated by solution,
				if specific_variable is not None, only constraints related to it are considered
		"""
		violations = []
		for constraint in self.constraints:
			if constraint.is_soft():
				continue # skip soft constraints 

			if specific_variable is not None and specific_variable not in constraint.variables:
				continue # skip if specific_variable is set, and constraint isn't related to it
				
			pass_test = constraint.test(solution)
			if not pass_test:
				violations.append(constraint)

		return violations

