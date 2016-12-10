import graph
import json
import pprint

#Read in a JSON file containing the class and student information.
student_json = open('students.json')
student_data = json.load(student_json)
student_json.close()

#Build a flow graph from the information in the JSON file.
flow_graph = graph.ResidualGraph()
flow_graph.add_node('source')
flow_graph.add_node('sink')

#add all the courses and connect them to their times, weight of capacity
for course in student_data['classes']:
	flow_graph.add_node(course['name'])
	for time in course['times']:
		flow_graph.add_node(time)
		flow_graph.add_edge(course['name'], time, course['capacity'])
		#connect times to sink, edge weight of 1
		flow_graph.add_edge(time, 'sink', 1)

#connect source to students, edge weight of number of classes
for student in student_data['students']:
	flow_graph.add_node(student['name'])
	flow_graph.add_edge('source', student['name'], len(student['classes']))
	for course in student['classes']:
		#connect student to courses, edge weight of 1
		flow_graph.add_edge(student['name'], course, 1)

#Find the maximum flow through the graph (from source to sink), giving the maximum number of classes that can be scheduled by all students.
flow_graph.ford_fulkerson()

#Using the information about the maximum flow through the graph, output the students’ schedules in a JSON file.
schedules = {}
schedules['students'] = []
for student in student_data['students']:
	temp_stud = {}
	temp_stud['name'] = student['name']
	temp_stud['classes'] = []
	for course in student['classes']:
		class_data = {}
		class_data['name'] = course
		for edge in flow_graph.edge_list[course]:
			if edge.flow > 0:
				class_data['time'] = edge.right
		temp_stud['classes'].append(class_data)
	schedules['students'].append(temp_stud)
	
with open('schedules.json', 'w') as fp:
	json.dump(schedules, fp)