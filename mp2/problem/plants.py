from problem.problem import Problem 
from problem.constraints import *

def problem():
	# Variables
	variables = ['C','R','S','T','V']
	C,R,S,T,V = variables
	# C = corpse, R = rose, S = sunflower, T = tulip, V = vampire
	
	# Domain
	domain = {}
	for var in variables:
		domain[var] = [1,2,3,4,5] # pot numbers

	# Constraints
	constraints = []

	# 1) one plant per pot
	c = AllDifferent(variables)
	c.name = 'AllDiff'
	constraints.append(c)

	# 2) rose cannot be adjacent to corpse
	c = NotNextTo([R,C])
	c.name = '|R-C|>1'
	constraints.append(c)

	# 3) rose must be closer to door than corpse
	c = CloserToDoor([R,C])
	c.name = 'R<C'
	constraints.append(c)

	# 4) vampire cannot be adjacent to rose, sunflower, tulip
	for plant in [R,S,T]:
		c = NotNextTo([V,plant])
		c.name = '|V-%s|>1' % plant
		constraints.append(c)

	# 5) At least 2 pots between vampire and sunflower
	c = MinDistance([V,S],3)
	c.name = '|V-S|>=3'
	constraints.append(c)

	# All hard constraints
	for c in constraints:
		c.penalty = float('inf')

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'Plants'
	problem.solution_format = solution_format

	return problem

def solution_format(problem,solution):
	# Initialize pots
	pots = problem.domain[problem.variables[0]]
	pot_contents = {}
	for pot in pots:
		pot_contents[pot] = []

	# Group into pots
	for plant,pot in solution.items():
		pot_contents[pot].append(plant)

	# Format output
	output = []
	output.append('\t')
	for pot in pots:
		content = ','.join(pot_contents[pot]).ljust(10)
		output.append(content)
	output.append('\n')
	output.append('\t')
	for pot in pots:
		output.append(str(pot).ljust(10))

	return ''.join(output)

