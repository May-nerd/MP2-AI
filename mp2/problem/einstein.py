from problem.problem import Problem 
from problem.constraints import *

def problem():
	# Einstein's Puzzle 
	colors = 'yellow red green blue white'.split()
	yellow,red,green,blue,white = colors

	nationalities = 'norwegian danish british german swedish'.split()
	norwegian,danish,british,german,swedish = nationalities

	beverages = 'water tea milk coffee beer'.split()
	water,tea,milk,coffee,beer = beverages

	socials = 'facebook twitter instagram snapchat g+'.split()
	facebook,twitter,instagram,snapchat,gplus = socials

	pets = 'cat horse bird fish dog'.split()
	cat,horse,bird,fish,dog = pets

	# Variables
	variables = colors + nationalities + beverages + socials + pets
	variable_groups = [colors,nationalities,beverages,socials,pets]
	group_names = ['colors','nationalities','beverages','socials','pets']
	
	# Domain
	domain = {}
	for variable_group in variable_groups:
		for var in variable_group:
			domain[var] = [1,2,3,4,5] # house numbers

	# Constraints
	constraints = []

	# 1) AllDifferent 
	for i,variable_group in enumerate(variable_groups):
		c = AllDifferent(variable_group)
		c.name = 'AllDiff:%s' % group_names[i]
		constraints.append(c)

	# 2) british == red
	c = BinaryEqual([british,red])
	c.name = 'british == red'
	constraints.append(c)

	# 3) swedish == dog
	c = BinaryEqual([swedish,dog])
	c.name = 'swedish == dog'
	constraints.append(c)

	# 4) danish == tea
	c = BinaryEqual([danish,tea])
	c.name = 'danish == tea'
	constraints.append(c)

	# 5) green == coffee
	c = BinaryEqual([green,coffee])
	c.name = 'green == coffee'
	constraints.append(c)

	# 6) facebook == bird
	c = BinaryEqual([facebook,bird])
	c.name = 'facebook == bird'
	constraints.append(c)

	# 7) yellow == twitter
	c = BinaryEqual([yellow,twitter])
	c.name = 'yellow == twitter'
	constraints.append(c)

	# 8) instagram == beer
	c = BinaryEqual([instagram,beer])
	c.name = 'instagram == beer'
	constraints.append(c)

	# 9) german == snapchat
	c = BinaryEqual([german,snapchat])
	c.name = 'german == snapchat'
	constraints.append(c)

	# 10) neighbors(g+,cat)
	c = Neighbors([gplus,cat])
	c.name = 'neighbors(g+,cat)'
	constraints.append(c)

	# 11) neighbors(horse,twitter)
	c = Neighbors([horse,twitter])
	c.name = 'neighbors(horse,twitter)'
	constraints.append(c)

	# 12) neighbors(norwegian,blue)
	c = Neighbors([norwegian,blue])
	c.name = 'neighbors(norwegian,blue)'
	constraints.append(c)

	# 13) neighbors(gplus,water)
	c = Neighbors([gplus,water])
	c.name = 'neighbors(gplus,water)'
	constraints.append(c)

	# 14) green is left neighbor of white
	c = LeftNeighbor([green,white])
	c.name = 'left neighbor(green,white)'
	constraints.append(c)

	# 15) milk == 3
	c = ValueEqual(milk,3)
	c.name = 'milk == 3'
	constraints.append(c)

	# 16) norwegian == 1
	c = ValueEqual(norwegian,1)
	c.name = 'norwegian == 1'
	constraints.append(c)

	# All hard constraints
	for c in constraints:
		c.penalty = float('inf')

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = "Einstein's Puzzle"
	problem.variable_groups = variable_groups
	problem.solution_format = solution_format

	return problem

def solution_format(problem,solution):
	# Initialize houses
	houses = problem.domain[problem.variables[0]]
	house_contents = {}
	for house in houses:
		house_contents[house] = []

	# Group into houses
	for variable_group in problem.variable_groups:
		for variable in variable_group:
			house = solution[variable]
			house_contents[house].append(variable)

	# Format output
	output = []
	for house in houses:
		output.append('\t')
		output.append(str(house).ljust(5))
		for content in house_contents[house]:
			output.append(content.ljust(15))
		output.append('\n')

	return ''.join(output)

	