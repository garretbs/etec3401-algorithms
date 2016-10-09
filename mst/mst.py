import mapviewer
import graph
import math


#Read in and parse the palace/town names and pixel coordinates from the hyrule.json file
hyrule_graph = mapviewer.hyrule_data

palaces = {} #super-graph of all graphs, for convenience
#Build a graph for each palace
# a) The vertices of each graph will be the palace and all of the towns
for palace in hyrule_graph['palaces']:
	towns_graph = {} #the graph representing a particular palace and its towns
	towns_graph[palace] = []
	for town1 in hyrule_graph['towns']:
	# b) The graph will have edges from the palace to each town
	# d) The edges of this graph will be weighted using Euclidean (straight-line) distance for the weights. You will use the palace/town pixel coordinates to calculate this distance.
		town_data = (town1, graph.dist(hyrule_graph['palaces'][palace], hyrule_graph['towns'][town1]))
		towns_graph[palace].append(town_data)
		towns_graph[town1] = []
		town_data = (palace, graph.dist(hyrule_graph['palaces'][palace], hyrule_graph['towns'][town1]))
		towns_graph[town1].append(town_data)
		for town2 in hyrule_graph['towns']:
			# c) The graph will have edges from each town to all other towns
			if town1 != town2:
				town_data = (town2, graph.dist(hyrule_graph['towns'][town1], hyrule_graph['towns'][town2]))
				towns_graph[town1].append(town_data)
	palaces[palace] = towns_graph

#Find the MST with the smallest sum of edge weights and pass the edges of this tree to the MapViewer.jarJava program. This will display a map of Hyrule with the tree drawn (as lines) on top of it.
smallest_weight = math.inf
smallest_graph = None
for palace in palaces:
	#Using Prim’s or Kruskal’s Algorithm, build a minimum spanning tree (MST) for each graph
	palaces[palace] = graph.prims_algorithm(palaces[palace])
	tsmallest = graph.sum_of_weights(palaces[palace])
	if  tsmallest < smallest_weight:
		smallest_weight = tsmallest
		smallest_graph = palace
mapviewer.import_coordinates(palaces[smallest_graph])