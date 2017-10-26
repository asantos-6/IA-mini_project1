import networkx as nx
import matplotlib.pyplot as plt
from datetime import date
from disjoint_union import *

DOC = "mir.txt"
STATION_PLANT = nx.Graph()
STATION_ELEMENTS = []
LAUNCH_GRAPH = nx.Graph()
NEXT_STATES = []
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
        self.max_payload = max_payload
        self.fixed_cost = fixed_cost
        self.variable_cost = variable_cost

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
    def __init__(self, launch, elements): #''', path, cost):
        self.launch = launch
        self.elements = elements
        #self.path = path
        #self.cost = cost

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
        e.adj_list = find_adj_node(e.ID)

    return STATION_ELEMENTS, Edges, Launches, STATION_PLANT

def state_adj_list(element_list):
    adj_list = []
    i = 0
    adj_list = disjoint_union(element_list[0].adj_list, element_list[1].adj_list)

    for i in range(2, len(element_list)):
        adj_list = disjoint_union(element_list[i].adj_list, adj_list)

    for y in element_list:
        adj_list = list(filter(lambda x: x.ID != y.ID, adj_list))

    return adj_list

def expand_state(previous_state, max_payload):
    new_states = []
    if previous_state.launch == 0:
        previous_element_list = []
        open_list = STATION_ELEMENTS
    else:
        previous_element_list = list(previous_state.elements)
        open_list = state_adj_list(previous_element_list)

    new_states = combine_elements(previous_state.launch+1, open_list, previous_element_list, [], max_payload)
    new_states = list(set(new_states))

    return new_states

def combine_elements (launch, elements, previous_element_list, next_states, max_payload):
    total_weight = 0
    new_elements = []
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
        new_states = []
        total_weight = e.weight
        for x in previous_element_list:
            total_weight = total_weight + x.weight

        if total_weight < max_payload:
            new_elements = list(previous_element_list)
            new_states = list(next_states)

            already_there = 0
            for x in new_elements:
                if x.ID == e.ID:
                    already_there = 1
                    break
            if not already_there:
                new_elements.append(e)
            '''
            print("New Elements:")
            for e in new_elements:
                print(e.ID)
            print("")
            '''
            new_state = State(launch, new_elements)
            new_state.elements.sort(key=lambda x: x.ID)
            if len(new_elements) == 1:
                elements = list(new_elements[0].adj_list)
            else:
                elements = state_adj_list(new_elements)
            for e in elements:
                if not e.adj_list:
                    e.adj_list = find_adj_node(e.ID)

            already_there = 0
            for n in new_states:
                if new_state == n:
                    already_there = 1
                    break
            if not already_there:
                new_states.append(new_state)
                NEXT_STATES.append(new_state)
                #NEXT_STATES = list(set(NEXT_STATES))
            '''
            print("New States:")
            for n in new_states:
                print(n.launch, end = ": ")
                for e in n.elements:
                    print(e.ID, end = " ")
                print("")
            print("")
            '''
            new_states.extend(combine_elements(launch, elements, new_elements, new_states, max_payload))

    if not new_elements or already_there:
        return []
    else:
        new_states = list(set(new_states))
        return new_states

def find_adj_node(node):
    node_key = STATION_PLANT[node]
    node_list = []
    elements = list(STATION_ELEMENTS)
    for key in node_key.keys():
        for e in elements:
            if e.ID == key:
                element = Element(key, float(e.weight))
                node_list.append(element)
                elements.remove(e)
                break
    return node_list


def main():
    STATION_ELEMENTS, E, L, STATION_PLANT = read_doc(DOC)

    init = State(0, STATION_ELEMENTS)
    first_launch = expand_state(init, 140)
    for x in first_launch:
        print(x.launch, end = ':')
        for e in x.elements:
            print(" ", e.ID, end = ',')
        print("")

    #(PESOS)
    #for e in STATION_ELEMENTS:
        #print(e.get_element(), "->", e.adj_list)
    #print(STATION_PLANT)
    #for node in STATION_PLANT:
        #print (node.get_element())
    '''
    init = State(1,['VCM'])
    print (init.get_info("all"))

    node_list = find_adj_node('VCM')

    print (node_list)
    node_list = ['VS', 'VK1', 'VK2']
    all_states = find_all_next_states(init, init.get_info("e"), node_list, 22.8, 5)
    for a in range(0,len(all_states)):
        all_states[a].print_state()

    print (init)
    '''

if __name__ == "__main__":
    main()
