import math

def prims_algorithm(graph):
	edge_list = []
	new_graph = {}
	start_node = list(graph.keys())[0]
	
	#put start node's edges in a list
	for edge in graph[start_node]:
		edge_list.append((start_node, edge[0], edge[1]))
		
	while len(new_graph) < len(graph): #stop once all vertices are in the new tree
	
		#pick the smallest edge, add the connecting node to the graph
		smallest = get_smallest_edge(edge_list)
		edge_list.remove(smallest)
		#so we've got the smallest, but what if both nodes are already in the graph?
		while smallest[0] in new_graph and smallest[1] in new_graph:
			smallest = get_smallest_edge(edge_list)
			edge_list.remove(smallest)
		
		#add the new smallest edge to the graph, checking if either node is already added
		if smallest[0] not in new_graph:
			new_graph[smallest[0]] = []
		new_graph[smallest[0]].append((smallest[1], smallest[2]))
		if smallest[1] not in new_graph:
			new_graph[smallest[1]] = []
		new_graph[smallest[1]].append((smallest[0], smallest[2]))
		
		#add new node's edges to the edge list, check for redundancy
		for edge in graph[smallest[1]]:
			if (edge[0], smallest[1], edge[1]) not in edge_list:
				edge_list.append((smallest[1], edge[0], edge[1]))
	return new_graph
	
def sum_of_weights(graph):
	total = 0
	for node in graph:
		for i in range(len(graph[node])):
			total += graph[node][i][1]
	total *= 0.5 #divide by 2 because each edge is counted twice exactly
	return total
	
def get_smallest_edge(edge_list):
	smallest_edge = (None, None, math.inf)
	for edge in edge_list:
		if edge[2] < smallest_edge[2]:
			smallest_edge = edge
	return smallest_edge

def dist(coord1, coord2):
	x1,y1 = coord1
	x2,y2 = coord2
	return math.sqrt((x2-x1)**2 + (y2-y1)**2)