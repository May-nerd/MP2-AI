from problem.problem import Problem 
from problem.constraints import *

class Item:
	def __init__(self,number,value,weight):
		self.number = number
		self.value = value 
		self.weight = weight

	def __repr__(self):
		return '[%d, P%d, %dK]' % (self.number,self.value,self.weight)

	def __lt__(self,other):
		return self.number < other.number

	def __eq__(self,other):
		return self.number == other.number

	def __hash__(self):
		return id(self)

def problem(test_case):
	V,W,capacity = get_test_case(test_case)

	# Variables
	variables = []
	for i in range(len(V)):
		value = V[i]
		weight = W[i]
		item = Item(i,value,weight)
		variables.append(item)

	# Domain 
	domain = {}
	for var in variables:
		domain[var] = [0,1] # include or not

	# Constraints
	constraints = []

	# Knapsack Capacity
	c = KnapsackCapacity(variables,capacity)
	c.name = 'Capacity: %dK' % capacity
	c.penalty = float('inf') # hard
	constraints.append(c)

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'Knapsack - %d' % test_case
	problem.capacity = capacity 
	problem.total_value = sum([item.value for item in variables])
	problem.solution_format = solution_format

	return problem

def solution_format(problem,solution):
	output = []
	total_weight = 0
	total_value = 0

	output.append('\t' + 'In'.ljust(7))
	for item in problem.variables:
		if solution[item] == 1: # included
			content = '[P%d, %dK]' % (item.value,item.weight)
			total_weight += item.weight
			total_value += item.value
		else:
			content = ''
		output.append(content.ljust(15))
	output.append('\n')

	output.append('\t' + 'Out'.ljust(7))
	for item in problem.variables:
		if solution[item] == 0: # not included
			content = '[P%d, %dK]' % (item.value,item.weight)
		else:
			content = ''
		output.append(content.ljust(15))
	output.append('\n')

	output.append('\t' + 'Weight'.ljust(7))
	output.append('%d / %d' % (total_weight,problem.capacity))
	output.append('\n')

	output.append('\t' + 'Value'.ljust(7))
	output.append('P%d' % total_value)

	return ''.join(output)

def get_test_case(test_case):
	if test_case == 0:
		V = [15,10,9,5]
		W = [1,5,3,4]
		capacity = 8
	elif test_case == 1:
		V = [4,2,2,1,10]
		W = [12,1,2,1,4]
		capacity = 15 
	elif test_case == 2:
		V = [61, 49, 37, 31, 70, 28, 43, 4, 52, 7, 46, 16, 64, 10, 73]
		W = [4, 9, 15, 16, 19, 8, 18, 3, 13, 11, 7, 1, 14, 6, 17]
		capacity = 80
	elif test_case == 3:	
		V = [7, 13, 91, 5, 39, 23, 97, 87, 11, 57, 37, 75, 69, 17, 43, 51, 25, 41, 21, 85]
		W = [7, 8, 17, 19, 22, 3, 13, 4, 23, 30, 9, 20, 2, 25, 6, 14, 11, 18, 27, 12]
		capacity = 150
	elif test_case == 99:
		V = [114, 70, 99, 82, 71, 112, 29, 14, 31, 107, 39, 56, 72, 22, 61, 19, 100, 13, 25, 59, 23, 67, 32, 65, 78, 116, 8, 105, 21, 44, 10, 111, 80, 51, 18, 52, 89, 2, 46, 45, 16, 28, 30, 101, 96, 74, 11, 92, 34, 55]
		W = [4, 39, 56, 38, 53, 37, 52, 69, 28, 24, 2, 16, 27, 73, 49, 8, 25, 71, 40, 31, 14, 75, 42, 18, 5, 63, 48, 7, 60, 59, 30, 36, 1, 50, 3, 33, 61, 68, 55, 22, 32, 34, 44, 17, 46, 54, 13, 12, 58, 19]
		capacity = 700
		
	return V,W,capacity