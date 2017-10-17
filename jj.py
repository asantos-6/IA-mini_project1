import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import Counter

DOC = "mir.txt"
G = nx.Graph()
PESOS = dict()
BUG = 0

def increment():
    BUG += 1
    return

class State:

    def __init__(self, launch, elements_on_space):
        self.Launch = launch
        self.Elements = elements_on_space
        self.Cost = 0

        return

    def getter(self):
        a = [self.Launch,self.Elements]
        return a

    def get_element(self):
        return self.Elements

    def get_launch(self):
        return self.Launch

    def print_state(self):
        print ("state print:",self.Launch, self.Elements)
        return

    def compare(s,t):
        return Counter(s) == Counter(t)

    def compareState(a,b):
        if(a.Launch == b.Launch & compare(a.Elements,b.Elements)):
            return True
        else:
            return False


def read_doc(doc_name):

    Vertices = []                   #vetor de vertices do satelite
    Edges = []                      #vetor de edge dos satelite
    Weight = []                     #vetor de peso de componentes de satelite
    launch_datas = []               #lista de lista onde contem as informacoes acerca de cada launch, cada lista contem max weight, fixed cost e variable cost

    launch_info1 = []
    launch_info2 = []
    launch_info3 = []
    
    f = open(doc_name)
    line = f.readline()
    while line:
        line = line.replace("\n","")
        words = line.split(" ")
        if(words[0] != ""):
            if(words[0][0] == "V"):
                G.add_node(words[0])
                Vertices.append(words[0])
                Weight.append(float(words[1]))
            if(words[0][0] == "E"):
                edge_pair = []
                edge = (words[1], words[2])
                edge_pair.append(words[1])
                edge_pair.append(words[2])
                G.add_edge(*edge)
                Edges.append(edge_pair)
            if(words[0][0] == 'L'):
                launch_info1.append(float(words[2]))
                launch_info2.append(float(words[3]))
                launch_info3.append(float(words[4]))
        line = f.readline()

    launch_datas.append(launch_info1)
    launch_datas.append(launch_info2)
    launch_datas.append(launch_info3)
    

    '''
    nx.draw(G,with_labels = True)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
    '''
    for x in range(0,len(Vertices)):
        PESOS[Vertices[x]] = Weight[x]

    return Vertices, Edges, launch_datas, G


def isInList(list_a, b):
    for e in list_a:
        if State.compareState(e,b):
            return True
    return False

def addInexistenceState(list_a, list_b):
    for s in list_b:
        if not isInList(list_a,s):
            list_a.append(s)



def find_all_next_states(actual_state, launched_nodes, adj_nodes, max_payload, act_weight):
    next_states = []

    if (len(adj_nodes) > 0):
        
        new_elements = actual_state.get_element()
        for x in range(0, len(adj_nodes)):
            component_weight = PESOS[adj_nodes[x]]
            if ((act_weight+component_weight <= max_payload)):
                    if (len(adj_nodes) ==3):
                        print ("--------------primeira chamada---------------", new_elements)
                    
                    new_elements = list(actual_state.get_element())
                    new_elements.append(adj_nodes[x])
                    new_elements1 = list(new_elements)
                    current_state = State(actual_state.get_launch(),new_elements1)
                    next_states.append(current_state)
                    del new_elements[-1]

                    print (current_state.getter())
                    
                    new_launched_nodes = list(launched_nodes)
                    new_launched_nodes.append(adj_nodes[x])

                    new_adj_nodes = list(adj_nodes)
                    del new_adj_nodes[x]

                    adj_list = find_adj_node(adj_nodes[x])

                    new_act_weight = act_weight + float(PESOS[adj_nodes[x]])

                    addInexistenceState(next_states,find_all_next_states(current_state, new_launched_nodes, new_adj_nodes, max_payload, new_act_weight))

    return next_states


def find_adj_node(node):
    node_key = G[node]
    node_list = []
    for key in node_key.keys():
        node_list.append(key)
    #print (node_list)
    return node_list


def compare(s,t):
    return Counter(s) == Counter(t)



def findAllLaunchStates(actual_state, launched_nodes, adj_nodes, total_launch,launch_info):
    all_states = []
    all_states_in_launch = []
    all_states_in_launch.append(actual_state)
    for x in range(0,total_launch):
        for y in range(0,len(all_states_in_launch)):
            states = find_all_next_states(all_states_in_launch[y], launched_nodes, adj_nodes, launch_info[x][0], 0)
    print (len(states))
    for a in states:
        a.print_state()

def main():
    V, E, L, G = read_doc(DOC)
    print(PESOS)

    init = State(1,[])
    node_list = ['VS', 'VK1', 'VK2', 'VP', 'VPM', 'VSTM', 'VK', 'VDM']
    findAllLaunchStates(init,  init.get_element(), node_list,1,L)




if __name__ == "__main__":
    main()
