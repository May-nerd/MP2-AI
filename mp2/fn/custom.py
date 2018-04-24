import random

### CUSTOM NEIGHBOR GENERATORS ###

def maxone_neighbor_generator(state):
    problem = state.problem
    solution = state.solution

    while True:
        neighbor = state.copy()

        # Flip a random 0 to 1
        value = None
        while value != 0:
            # randomly select var with value 0 assigned in solution
            var = random.choice(problem.variables)
            value = solution[var]

        new_value = 1
        neighbor.solution[var] = new_value
        neighbor.changes = [(var,new_value)]
        yield neighbor


def knapsack_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]
    while True:
        neighbor = state.copy()
        if(constraint.test(solution)):
            value1 = None
            value2 = None
            var1 = random.choice(problem.variables)
            value1 = solution[var1]
            var2 = random.choice(problem.variables)
            value2 = solution[var2]

            if(value1 == 1):
                if(var1 == var2):
                    #removing the item
                    new_value = 0
                    neighbor.solution[var1] = new_value
                    neighbor.changes = [(var1, new_value)]
                else:
                    #swap the items
                    while value2 !=0:
                        var2 = random.choice(problem.variables)
                        value2 = solution[var2]

                    temp = neighbor.solutions[var1]
                    neighbor.solution[var1] = neighbor.solution[var2]
                    neighbor.solution[var2] = temp
                    neighbor.changes = [(var1, neighbor.solution[var1]), (var2, neighbor.solution[var2])]
            else:
                if(var1 == var2):
                    #add the item
                    new_value = 1
                    neighbor.solution[var1] = new_value
                    neighbor.changes = [(var1, new_value)]
                else:
                    #swap the items
                    while value2 !=1:
                        var2 = random.choice(problem.variables)
                        value2 = solution[var2]
                    temp = neighbor.solutions[var1]
                    neighbor.solution[var1] = neighbor.solution[var2]
                    neighbor.solution[var2] = temp
                    neighbor.changes = [(var1, neighbor.solution[var1]), (var2, neighbor.solution[var2])]
        else:
            #remove the item
            new_value = 0
            value = None
            while value != 1:
                var = random.choice(problem.variables)
                value = solution[var]
            print(var)
            neighbor.solution[var] = new_value
            neighbor.changes = [(var, new_value)]
            print(neighbor)
        yield neighbor

        # INSERT CODE HERE
        # Idea: If knapsack is already full, neighbor = remove a random item from current solution (try to remove excess)
        #       If knapsack is not yet full, neighbor = randomly change up to 2 values (includes adding item, removing item, swapping)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        # yield neighbor


def vertex_cover_neighbor_generator(state):
    problem = state.problem
    solution = state.solution
    constraint = problem.constraints[0]

    while True:
        neighbor = state.copy()

        # INSERT CODE HERE
        # Idea: If all edges not yet covered, neighbor = add a random vertex to current solution (try to add more edges covered)
        #       If all edges already covered, neighbor = remove a random vertex from current solution (try to minimize no. of vertex used)
        # Hint: use constraint.test(solution)
        # Hint: check the pattern of maxone_neigbor_generator
        # Dont forget to update neighbor.changes
        # yield neighbor
