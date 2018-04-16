class Constraint:
	def __init__(self,variables,penalty=None):
		self.variables = variables
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def __repr__(self):
		return 'Constraint:%s' % self.name

	def is_hard(self):
		return self.penalty == float('inf')

	def is_soft(self):
		return not self.is_hard()

	def get_assigned_values(self,solution):
		values = []
		for var in self.variables:
			if var in solution:
				values.append(solution[var])
		return values

class BinaryConstraint(Constraint):
	def test(self,solution):
		var1,var2 = self.variables
		if var1 in solution and var2 in solution:
			# both vars assigned
			value1 = solution[var1]
			value2 = solution[var2]
			# BinaryConstraints will implement binary_test
			return self.binary_test(value1,value2)
		else:
			# dont test if one var is unassigned
			return True

### Global Constraints ###

class AllDifferent(Constraint):
	def test(self,solution):
		values = self.get_assigned_values(solution)

		num_values = len(values)
		num_unique = len(set(values))

		# if no duplicates, orig list length = set(list) length
		return num_values == num_unique

### Plant Exhibit Constraints ###

class NotNextTo(BinaryConstraint):
	def binary_test(self,x,y):
		# if next to each other, abs diff == 1
		return not abs(x-y) == 1

class CloserToDoor(BinaryConstraint):
	def binary_test(self,x,y):
		# x is closer to door if its pot no. is lower than y
		return x < y

class MinDistance(BinaryConstraint):
	def __init__(self,variables,minimum,penalty=0):
		self.variables = variables
		self.minimum = minimum
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def binary_test(self,x,y):
		# distance is at least self.minimum
		return abs(x-y) >= self.minimum

### Einstein's Problem Constraints ###

class ValueEqual(Constraint):
	def __init__(self,variable,value,penalty=0):
		self.variable = variable
		self.variables = [variable] # to conform with Constraint class
		self.value = value
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def test(self,solution):
		var = self.variable
		if var in solution:
			# check if assigned value == target value
			return solution[var] == self.value
		else:
			# dont test if var is unassigned
			return True

class BinaryEqual(BinaryConstraint):
	def binary_test(self,x,y):
		return x == y

class Neighbors(BinaryConstraint):
	def binary_test(self,x,y):
		# if neighbors, abs diff == 1
		return abs(x-y) == 1

class LeftNeighbor(BinaryConstraint):
	def binary_test(self,x,y):
		# if neighbors, abs diff == 1
		# x is left neighbor if x < y
		return abs(x-y) == 1 and x < y

### Magic Square Constraints ###

class ExactSum(Constraint):
	def __init__(self,variables,target_sum,penalty=0):
		self.variables = variables
		self.target_sum = target_sum
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def test(self,solution):
		values = self.get_assigned_values(solution)
		# INSERT CODE HERE
		# test only if all vars are assigned
		# check if sum of values is the target sum
		# dont test if not all vars assigned
		# return True / False

		# for var in self.variables:
		# 	print(var)
			# if(values[var] is None):
			# 	return False
			# sum = sum + values[var]

		if len(values) != 3:
			return False

		sum = 0
		for val in values:
			sum = sum + val

		return sum == self.target_sum
		


### Magic Series Constraints ###

class MagicSeries(Constraint):
	def test(self,solution):
		values = self.get_assigned_values(solution)

		if(len(values) != len(self.variables)):
			return True

		for var in self.variables:
			if(values.count(var) != values[var]):
				return False

		return True
		# INSERT CODE HERE
		# test only if all vars assigned
		# check that each index follows magic series property
		# Example: if 3 is assigned to index 0, there must be three 0s in the series
		# Example: if 2 is assigned to index 1, there must be two 1s in the series
		# dont test if not all vars assigned
		# return True / False

### Knapsack Constraints ###

class KnapsackCapacity(Constraint):
	def __init__(self,variables,capacity,penalty=0):
		self.variables = variables
		self.capacity = capacity
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def test(self,solution):
		# INSERT CODE HERE
		# can perform test even if not all variables are assigned (partial solutions allowed)
		# make sure to skip unassigned variables
		# check that total weight of items included in solution doesn't exceed capacity
		# return True / False
		total_weight = 0


### Vertex Cover Constraints ###

class VertexCover(Constraint):
	def __init__(self,variables,edges,penalty=0):
		self.variables = variables
		self.edges = edges
		self.penalty = penalty or float('inf') # hard, if penalty undefined
		self.name = 'undefined'

	def test(self,solution):
		# INSERT CODE HERE
		# test only if all vars assigned
		# check that all edges are covered by at least one vertex in the solution
		# covered edge = at least one of the endpoints is a vertex that is in the solution
		# if at least one edge is not covered --> fail
		# dont test if not all vars assigned
		# return True / False
		active_vertices = []
		if(len(solution) == len(self.variables)):
			for key,value in solution.items():
				if(value == 1):
					active_vertices.append(key)
			for edge in self.edges:
				if(not (edge[0] in active_vertices or edge[1] in active_vertices)):
					return False
			return True
		else:
			return True
