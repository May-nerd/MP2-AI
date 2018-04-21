def maxone_fitness(state,feasibility_minimum):
	""" Fitness = no. of 1s """
	solution = state.solution
	score = sum(solution.values())
	# always add feasibility_minimum, since there are no constraints
	return feasibility_minimum + score

def knapsack_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	total_weight = 0
	total_value = 0
	for key,value in solution.items():
		if(value == 1):
			total_value = total_value + key.value
			total_weight = total_weight + key.weight

	if problem.find_hard_violation(solution) is not None: 
		# has violation: total weight exceeds capacity
		max_score = int(feasibility_minimum * 0.75)

		# INSERT CODE HERE
		# Idea: less excess weight = higher score
		# Hint: use item.weight, problem.capacity
		excess_weight = total_weight - problem.capacity
		return abs(max_score - excess_weight)

	else: 
		# no violations
		score = feasibility_minimum # min score for being valid solution

		# INSERT CODE HERE
		# Idea: higher total item value = higher score
		# Hint: use item.value

		return score + total_value

# KNAPSACK_FITNESS p4.py RESULT:
# Iteration: 201 -- LIMIT REACHED
# Best score: 1758
# Iterations: 201
# 1 solutions found



def vertex_cover_fitness(state,feasibility_minimum):
	problem = state.problem
	solution = state.solution

	if problem.find_hard_violation(solution) is not None: 
		# has violation: some edges are not covered
		max_score = int(feasibility_minimum * 0.75)
		used_vertices = [v for v in problem.variables if solution[v] == 1]

		# INSERT CODE HERE
		# Idea: less uncovered edges = higher score
		# Hint: use problem.edges, used_vertices
		uncovered_edge_count = 0
		for e in problem.edges:
			if(e[0] not in used_vertices and e[1] not in used_vertices):
				uncovered_edge_count = uncovered_edge_count + 1
				
		return max_score - uncovered_edge_count
	else:	
		# no violations
		score = feasibility_minimum # min score for being valid solution
		unused_vertices = [v for v in problem.variables if solution[v] == 0]

		# INSERT CODE HERE
		# Idea: less vertices used = better
		# So, higher no. of unused vertices in solution = higher score
		return score + len(unused_vertices)



# VERTEX_COVER p4.py RESULT:
# Iteration: 201 -- LIMIT REACHED
# Best score: 64
# Iterations: 201
# 1 solutions found
#         invalid   33   A,B,C,D,F,G,H,I,K,L,N,O,P,R,T,U,V,X,Z,e,f,g,h,j,l,p,q,r,s,u,v,w,y