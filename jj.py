import networkx as nx
import matplotlib.pyplot as plt
import sys
from datetime import date
from disjoint_union import *
from Graph_Search import *

#DOC = "trivial1.txt"
STATION_PLANT = nx.Graph()
STATION_ELEMENTS = []
LAUNCH_GRAPH = nx.Graph()
#PESOS = dict()

def increment():
    BUG += 1
    return

class Element:
    def __init__(self, ID, weight):
        self.ID = ID
        self.weight = weight
        self.adj_list = []

    def get_element(self):
        return self.ID
    def get_weight(self):
        return self.weight

class Edge:
    def __init__(self, element1, element2):
        self.element1 = element1
        self.element2 = element2

class Launch:
    def __init__(self, launch_date, max_payload, fixed_cost, variable_cost):
        self.launch_date = launch_date
        self.max_payload = float(max_payload)
        self.fixed_cost = float(fixed_cost)
        self.variable_cost = float(variable_cost)

    def get_info(self, mode):
        if mode == "d":
            return self.launch_date
        if mode == "p":
            return self.max_payload
        if mode == "f":
            return self.fixed_cost
        if mode == "v":
            return self.variable_cost


class State:
    def __init__(self, launch, elements, previous_state, cost):
        self.launch = launch
        self.elements = elements
        self.previous_state = previous_state
        self.cost = cost

        return

    def get_info(self, mode):
        if mode == "all":
            a = [self.launch,self.elements]
            return a
        if mode == "e":
            return self.elements
        if mode == "l":
            return self.launch
    '''
    def get_element(self):
        return self.Elements

    def get_launch(self):
        return self.Launch
    '''
    def print_state(self):
        print (self.Launch, self.Elements)
        return




def read_doc(doc_name):

    Edges = []                      #vetor de edge dos satelite
    Launches = []               #lista de lista onde contem as informacoes acerca de cada launch, cada lista contem max weight, fixed cost e variable cost

    f = open(doc_name)
    line = f.readline()
    while line:
        line = line.replace("\n","")
        words = line.split(" ")
        if(words[0] != ""):
            if(words[0][0] == "V"):
                element = Element(words[0], float(words[1]))
                STATION_PLANT.add_node(element)
                STATION_ELEMENTS.append(element)
            if(words[0][0] == "E"):
                edge = Edge(words[1], words[2])
                STATION_PLANT.add_edge(edge.element1, edge.element2)
                Edges.append(edge)
            if(words[0][0] == 'L'):
                words[1]
                launch = Launch(date(int(words[1][4:8]), int(words[1][2:4]), int(words[1][0:2])), float(words[2]), words[3], words[4])
                Launches.append(launch)
        line = f.readline()

    '''
    nx.draw(STATION_PLANT,with_labels = True)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
    '''
    Launches.sort(key=lambda r: r.launch_date)

    for e in STATION_ELEMENTS:
        e.adj_list = find_adj_node(e.ID, STATION_PLANT, STATION_ELEMENTS)

    return STATION_ELEMENTS, Edges, Launches, STATION_PLANT

def state_adj_list(element_list, problem):
    adj_list = []
    i = 0

    if len(element_list) == 1:
        adj_list = list(element_list[0].adj_list)

    else:
        adj_list = disjoint_union(element_list[0].adj_list, element_list[1].adj_list)
        for i in range(2, len(element_list)):
            adj_list = disjoint_union(element_list[i].adj_list, adj_list)

    for y in element_list:
        adj_list = list(filter(lambda x: x.ID != y.ID, adj_list))

    for e in adj_list:
        if len(e.adj_list) == 0:
            e.adj_list = find_adj_node(e.ID, problem.graph, problem.nodes)

    return adj_list

def Create_Childs(previous_state, problem):
    new_states = []
    if previous_state.launch == 0 or (previous_state.launch != 0 and not previous_state.elements):
        previous_element_list = []
        open_list = problem.nodes
    else:
        previous_element_list = previous_state.elements
        open_list = state_adj_list(previous_element_list, problem)
    if previous_state.launch < len(problem.actions):
        launch = problem.actions[previous_state.launch]

        new_states = combine_elements(launch, previous_state, open_list, previous_element_list, [], problem, 1)
        new_states.append(State(previous_state.launch+1, [], previous_state, 0))

        new_states = list(set(new_states))
        new_states.sort(key=lambda r: len(r.elements))


        return new_states

    else:
        return []

def combine_elements(launch, previous_state, elements, previous_element_list, next_states, problem, first):
    total_weight = 0
    launch_index = previous_state.launch+1
    new_elements = []
    for_states = []
    new_states = next_states
    '''
    print("Elements:")
    for e in elements:
        print(e.ID)

    print("Previous Element List:")
    for e in previous_element_list:
        print(e.ID)
    print("")
    '''
    for e in elements:
        total_weight = e.weight

        if not first:
            for x in previous_element_list:
                total_weight = total_weight + x.weight

        if total_weight <= launch.max_payload:
            new_elements = list(previous_element_list)


            if e not in new_elements:
                new_elements.append(e)
                new_elements.sort(key=lambda r: r.ID)

            adj_elements = state_adj_list(new_elements, problem)
            #elements.sort(key=lambda r: r.ID)
            '''
            print("New Elements:")
            for e in new_elements:
                print(e.ID)
            print("")

            print("New States:")
            for n in new_states:
                print(n.launch, end = ": ")
                for e in n.elements:
                    print(e.ID, end = " ")
                print("")
            print("")
            '''
            if adj_elements:
                new_states = (combine_elements(launch, previous_state, adj_elements, new_elements, new_states, problem, 0))


            insert = 1
            for n in for_states:
                if n.launch == launch_index and set(elementID_list(n.elements)) == set(elementID_list(new_elements)):
                    insert = 0
                    break
            if insert:
                new_state = State(launch_index, new_elements, previous_state, 0)
                new_states.append(new_state)
            for_states.extend(new_states)
    if not new_elements:
        return []
    else:
        #new_states = list(set(new_states))
        return for_states

def calc_cost(launch, state):
    if state.elements:
        if state.previous_state.launch == 0:
            element_list = state.elements
        else:
            element_list = disjoint_union(state.elements, state.previous_state.elements)
        cost = launch.fixed_cost
        for e in element_list:
            cost = cost + launch.variable_cost*e.weight
    else:
        return 0
    return cost


def elementID_list(element_list):
    ID_list =[]

    for e in element_list:
        ID_list.append(e.ID)

    return ID_list

def find_adj_node(node, station_plant, station_elements):
    node_key = station_plant[node]
    node_list = []
    elements = list(station_elements)
    for key in node_key.keys():
        for e in elements:
            if e.ID == key:
                element = Element(key, float(e.weight))
                node_list.append(element)
                elements.remove(e)
                break
    return node_list

def init_search(problem):
    init = State(0, problem.nodes, [], 0)
    first_launch = Create_Childs(init, problem)

    return first_launch

def Check_Goal(station_elements, state):
    if len(state.elements) == len(station_elements):
        return state
    else:
        return False

def print_solution(state):
    if state.previous_state:
        print_solution(state.previous_state)
    else:
        return
    print(state.launch, end = ':')
    element_list = disjoint_union(state.elements, state.previous_state.elements)
    for e in element_list:
        print(" ", e.ID, end = ',')
    print(" ", state.cost)

def main():
    DOC = sys.argv[1]
    STATION_ELEMENTS, E, L, STATION_PLANT = read_doc(DOC)

    '''GRAPH SEARCH'''

    problem = Problem(STATION_ELEMENTS, L, STATION_PLANT)
    goal = General_Search(problem, "uni")

    print_solution(goal)

    '''
    for x in first_launch:
        print(x.launch, end = ':')
        for e in x.elements:
            print(" ", e.ID, end = ',')
        print(" ", x.cost)
    '''

if __name__ == "__main__":
    main()
