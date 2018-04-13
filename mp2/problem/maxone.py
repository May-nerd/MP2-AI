from problem.problem import Problem 
from problem.constraints import *

def problem(N):
	# Variables
	variables = list(range(N))

	# Domain 
	domain = {}
	for var in variables:
		domain[var] = [0,1]

	# Constraints: None
	constraints = []

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'MaxOne(%d)' % N
	problem.N = N
	problem.solution_format = solution_format

	return problem

def solution_format(problem,solution):
	count = sum(solution.values())

	output = []
	output.append('\t' + str(count).ljust(5))
	for var in problem.variables:
		output.append(str(solution[var]))

	return ''.join(output)

