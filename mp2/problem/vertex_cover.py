from problem.problem import Problem 
from problem.constraints import *

def problem(test_case):
	vertices,edges = get_test_case(test_case)

	# Variables
	variables = vertices 

	# Domain
	domain = {}
	for var in variables:
		domain[var] = [0,1] # include or not

	# Constraints
	constraints = []

	# Vertex Cover
	c = VertexCover(variables,edges)
	c.name = 'Vertex Cover'
	c.penalty = float('inf') # hard
	constraints.append(c)

	# Create problem
	problem = Problem(variables,domain,constraints)
	problem.name = 'Vertex Cover - %d' % test_case
	problem.edges = edges
	problem.solution_format = solution_format

	return problem

def solution_format(problem,solution):
	constraint = problem.constraints[0]
	is_valid = 'valid' if constraint.test(solution) else 'invalid'

	active_vertices = []
	for vertex in problem.variables:
		if solution[vertex] == 1: 
			active_vertices.append(vertex)

	output = []
	output.append('\t' + is_valid.ljust(10))
	output.append(str(len(active_vertices)).ljust(5))
	output.append(','.join(active_vertices))

	return ''.join(output)

def get_test_case(test_case):
	if test_case == 0:
		vertices = 'A B C D E F'.split()
		edges = 'AB AD AE AF BC CD CE CF EF'.split()
	elif test_case == 1:
		vertices = 'A B C D E F G'.split()
		edges = 'AB BC CD CE DE DF DG EF'.split()
	elif test_case == 2:
		vertices = 'A B C D E F G H'.split()
		edges = 'AB BC CD DE EF FG GA HA HB HC HD HE HF HG'.split()
	elif test_case == 3:
		vertices = 'A B C D E F G H I'.split()
		edges = 'AB BC DE EF GH HI AD BE CF DG EH FI AE BF DH EI BD CE EG FH'.split()
	elif test_case == 4:
		vertices = 'A B C D E F G H I J'.split()
		edges = 'AB CD EF GH IJ AC CE EG GI IA BF BH JD JF DH'.split()
	elif test_case == 5:
		vertices = 'A B C D E F G H I J K L M N'.split()
		edges = 'AB AE BC BE BF CD CF CG DG DH EF EI EJ EK EL FG FI GH GI HI HJ HN IJ JL JM JN KL KM LM MN'.split()
	elif test_case == 99:
		vertices = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		edges = ['re', 'SR', 'bw', 'XK', 'WA', 'kI', 'dy', 'TY', 'zV', 'Qf', 'uR', 'vy', 'ea', 'Zt', 'aN', 'Da', 'oW', 'hA', 'UW', 'Ks', 'mU', 'nV', 'tU', 'Mu', 'jw', 'YV', 'Jm', 'sd', 'Es', 'Cc', 'Hi', 'fT', 'Bt', 'AL', 'LX', 'PW', 'Og', 'Nv', 'GF', 'RO', 'Vc', 'wM', 'FB', 'IU', 'lx', 'cI', 'iT', 'yq', 'pG', 'qi', 'xq', 'gv', 'UC', 'NV', 'Nr', 'zw', 'TX', 'kP', 'lE', 'fa', 'dP', 'KU', 'ZW', 'Au', 'pd', 'Lm', 'ZT', 'Qw', 'cu', 'DL', 'uB', 'Ga', 'aw', 'Ou', 'qJ', 'hO', 'de', 'qz', 'eu', 'jU', 'tj', 'PI', 'fA', 'yM', 'BS', 'xH', 'IM', 'Pm', 'uf', 'RD', 'gL', 'Un', 'Xb', 'jS', 'sD', 'tR', 'vz', 'vF', 'kS', 'kt', 'XU', 'Bq', 'ih', 'DE', 'ub', 'df', 'jK', 'ol', 'gW', 'Nu', 'iM', 'Wy', 'QB', 'em', 'wS', 'wF', 'KA', 'tG', 'ZA', 'rz', 'OY', 'Lh', 'iZ', 'fW', 'SE', 'Ix', 'ZV', 'zm', 'As', 'gi', 'FZ', 'ut', 'pe', 'dJ', 'dz', 'qw', 'ke', 'qP', 'ph', 'hb', 'kc', 'RZ', 'dX', 'Xz', 'wK', 'TW', 'sH', 'rE', 'hR', 'za']

	return vertices,edges