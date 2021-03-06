import random

### VARIABLE ORDERING FUNCTIONS ###

def first_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)
	return unassigned_vars[0]

def random_unassigned(state):
	problem = state.problem
	solution = state.solution

	unassigned_vars = problem.unassigned_variables(solution)
	return random.choice(unassigned_vars)

def custom_variable_selector(state):
	problem = state.problem
	solution = state.solution
	domain = state.domain

	# INSERT CODE HERE
	# Write your variable ordering code here
	# Return an unassigned variable

	unassigned_vars = problem.unassigned_variables(solution)
	# ++++++++++++++++++++++++++++++++++++++++
	# HEURISTIC 1
	minimum = unassigned_vars[0]
	if(len(domain[minimum]) == 0):
		return minimum

	for var in unassigned_vars:
		if(len(domain[var]) < len(domain[minimum])):
			minimum = var
	return minimum
	# ++++++++++++++++++++++++++++++++++++++++

	# ++++++++++++++++++++++++++++++++++++++++
	# HEURISTIC 2
	# maximum = unassigned_vars[0]
	# for var in unassigned_vars:
	# 	if(len(domain[var]) > len(domain[maximum])):
	# 		maximum = var
	# return unassigned_vars[0]
	# ++++++++++++++++++++++++++++++++++++++++



	# Suggestions:
	# Heuristic 1: minimum remaining values = select variables with fewer values left in domain
	# Heuristic 2: degree heuristic = select variables related to more constraints
	# Can use just one heuristic, or chain together heuristics (tie-break)

### VALUE ORDERING FUNCTIONS ###

def default_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain
	return values # return as-is

def random_order(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	values = domain[:] # make copy
	random.shuffle(values)
	return values

def custom_value_ordering(state,variable):
	problem = state.problem
	domain = state.domain[variable]

	if(len(domain) == 0):
		return domain

	num_domain = 0
	for d, v in state.domain.items():
		num_domain = num_domain + len(v)

	num_new_state = []
	for value in domain:
		new_state = state.copy()
		new_state.assign(variable, value)
		forward_checking(new_state, variable)

		temp = 0
		for d, v in new_state.domain.items():
			temp = temp + len(v)
		num_new_state.append(temp)

	num_new_state[:] = [num_domain - num for num in num_new_state]
	print(len(num_new_state))

	temp = {}
	for i in range(len(num_new_state)):
		temp[domain[i]] = num_new_state[i]

	import operator
	temp = sorted(temp.items(), key=operator.itemgetter(1))
	print(temp)

	new_domain = []
	for i in temp:
		new_domain.append(i[0])

	return new_domain
	# Suggestions:
	# Heuristic: least constraining value (LCV)
	# LCV = prioritize values that filter out fewer values in other variables' domains
	# Hint: you will use state.copy() for new_state, use new_state.assign, and use forward_checking() on new_state
	# Count the number of filtered values by comparing the total from current state and new_state

### FILTERING FUNCTIONS ###

def do_nothing(state,variable):
	problem = state.problem
	return # do nothing

def forward_checking(state,variable):
	problem = state.problem
	solution = state.solution

	for constraint in problem.constraints:
		if variable not in constraint.variables:
			continue # skip if unrelated to variable

		for other_var in constraint.variables:
			if other_var == variable: continue # skip self
			if other_var in solution: continue # skip assigned

			valid_values = []
			for value in state.domain[other_var]:
				new_solution = solution.copy()
				new_solution[other_var] = value

				pass_test = constraint.test(new_solution)
				if pass_test:
					valid_values.append(value)
			state.domain[other_var] = valid_values
