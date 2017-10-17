import networkx as nx
import matplotlib.pyplot as plt
from datetime import date

DOC = "mir.txt"
STATION_PLANT = nx.Graph()
LAUNCH_GRAPH = nx.Graph()
#PESOS = dict()
BUG = 0

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


class State:
    def __init__(self, launch, elements_on_space):
        self.Launch = launch
        self.Elements = elements_on_space

        return

    def getter(self):
        a = [self.Launch,self.Elements]
        return a

    def get_element(self):
        return self.Elements

    def get_launch(self):
        return self.Launch

    def print_state(self):
        print (self.Launch, self.Elements)
        return




def read_doc(doc_name):

    Vertices = []                   #vetor de vertices do satelite
    Edges = []                      #vetor de edge dos satelite
    #Weight = []                     #vetor de peso de componentes de satelite
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
                Vertices.append(element)
                #Weight.append(float(words[1]))
            if(words[0][0] == "E"):
                edge = Edge(words[1], words[2])
                #edge = (words[1], words[2])
                #edge_pair.append(words[1])
                #edge_pair.append(words[2])
                STATION_PLANT.add_edge(edge.element1, edge.element2)
                Edges.append(edge)
            if(words[0][0] == 'L'):
                words[1]
                launch = Launch(date(int(words[1][4:8]), int(words[1][2:4]), int(words[1][0:2])), words[2], words[3], words[4])
                Launches.append(launch)
                #launch_info.append(words[2])
                #launch_info.append(words[3])
                #launch_info.append(words[4])
        line = f.readline()

    '''
    nx.draw(STATION_PLANT,with_labels = True)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
    '''
    Launches.sort(key = lambda r: r.launch_date)

    for x in Vertices:
        x.adj_list = find_adj_node(x.get_element())
    #for x in range(0,len(Vertices)):
        #PESOS[Vertices[x]] = Weight[x]

    return Vertices, Edges, Launches, STATION_PLANT


def find_all_next_states(previous_node_list, actual_node, max_payload):
    for x in previous_node_list:
        print(x)
        current_weight = PESOS[actual_node] + PESOS[x]
        '''mudar esta merda

    if current_weight < max_payload:


    return next_states
    '''

def find_adj_node(node):
    node_key = STATION_PLANT[node]
    node_list = []
    for key in node_key.keys():
        node_list.append(key)
    #print (node_list)
    return node_list


def main():
    V, E, L, STATION_PLANT = read_doc(DOC)
    #print(PESOS)

    for x in V:
        print(x.get_element(), "->", x.adj_list)

    '''
    init = State(1,['VCM'])
    print (init.getter())

    node_list = find_adj_node('VCM')

    print (node_list)
    node_list = ['VS', 'VK1', 'VK2']
    all_states = find_all_next_states(init, init.get_element(), node_list, 22.8, 5)
    for a in range(0,len(all_states)):
        all_states[a].print_state()

    print (init)
    '''

if __name__ == "__main__":
    main()
