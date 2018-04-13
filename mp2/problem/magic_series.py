from problem.problem import Problem 
from problem.constraints import *

def problem(N):
	# Variables
	variables = list(range(0,N+1))

	# Domain
	domain = {}
	for var in variables:
		domain[var] = list(range(0,N+1))

	# Constraints
	constraints = []
	c = MagicSeries(variables)
	c.name = 'MagicSeries'
	c.penalty = float('inf')
	constraints.append(c)

	# Create problem 
	problem = Problem(variables,domain,constraints)
	problem.name = 'Magic Series(%d)' % N
	problem.N = N
	problem.solution_format = solution_format

	return problem 

def solution_format(problem,solution):
	output = []

	output.append('\t' + 'Index'.ljust(7))
	for index in problem.variables:
		output.append(str(index).ljust(5))
	output.append('\n')

	output.append('\t' + 'Series'.ljust(7))
	series = []
	for index in problem.variables:
		output.append(str(solution[index]).ljust(5))
		series.append(solution[index])
	output.append('\n')

	output.append('\t' + 'Count'.ljust(7))
	for index in problem.variables:
		count = series.count(index)
		output.append(str(count).ljust(5))
		
	return ''.join(output)

