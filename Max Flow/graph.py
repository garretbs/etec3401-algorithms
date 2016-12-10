class Edge(object):
	def __init__(self, left, right, capacity, back = False):
		self.left = left
		self.right = right
		self.capacity = capacity
		self.flow = 0
		if not back:
			back_edge = Edge(right, left, 0, True)
			self.back_edge = back_edge
			back_edge.back_edge = self
			
	def __repr__(self):
		if self.capacity > 0:
			return "%s -> %s <%i/%i>" % (self.left, self.right, self.flow, self.capacity)
		else:
			return "\t\t\t%s <- %s <%i/%i>" % (self.left, self.right, self.flow, self.capacity)
		
class ResidualGraph(object):
	def __init__(self):
		self.edge_list = {}
		
	def print_flows(self, node):
		for edge in self.edge_list[node]:
			print(edge)
		
	def find_path(self, left, right, path):
		if left == right:
			return path
		for edge in self.edge_list[left]:
			residual = edge.capacity - edge.flow
			if residual > 0 and edge not in path:
				new_path = self.find_path( edge.right, right, path + [edge]) 
				if new_path:
					return new_path
 
	def ford_fulkerson(self):
		path = self.find_path('source', 'sink', [])
		while path:
			flows = []
			for edge in path:
				flows.append(edge.capacity - edge.flow)
			flow = min(flows)
			for edge in path:
				edge.flow += flow
				edge.back_edge.flow -= flow
			path = self.find_path('source', 'sink', [])
		total_flow = 0
		for edge in self.edge_list['source']:
			total_flow += edge.flow
		return total_flow
		
	def add_node(self, node):
		if node not in self.edge_list:
			self.edge_list[node] = [];
		
	def add_edge(self, left, right, capacity):
		edge = Edge(left, right, capacity)
		self.edge_list[left].append(edge)
		self.edge_list[right].append(edge.back_edge)