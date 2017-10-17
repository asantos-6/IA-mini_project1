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
                launch_info = []
                launch_info.append(words[2])
                launch_info.append(words[3])
                launch_info.append(words[4])
        line = f.readline()

    '''
    nx.draw(G,with_labels = True)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display
    '''
    for x in range(0,len(Vertices)):
        PESOS[Vertices[x]] = Weight[x]

    return Vertices, Edges, launch_datas, G



def addInexistenceState(list_a, list_b):
    list_out = list(list_a)
    for s in list_b:
        for a in list_a:
            if not State.compareState(a,s):
                list_out.extend()



def find_all_next_states(actual_state, launched_nodes, adj_nodes, max_payload, act_weight):
    next_states = []

    if (len(adj_nodes) > 0):
        '''
        for x in range(0,len(adj_nodes)):
            if (element_weight[x] > max_payload):
                adj_nodes.remove(adj_nodes[x])
                element_weight.remove(element_weight[x])
        '''
        new_elements = actual_state.get_element()
        for x in range(0, len(adj_nodes)):
            if (len(adj_nodes) ==3):
                print ("--------------primeira chamada---------------", new_elements)
            print ("-----------------------------",adj_nodes[x])
            #actual_state.print_state()
            new_elements = list(actual_state.get_element())
            new_elements.append(adj_nodes[x])
            #print ("list",new_elements)
            new_elements1 = list(new_elements)
            current_state = State(actual_state.get_launch(),new_elements1)
            #current_state.print_state()
            next_states.append(current_state)
            del new_elements[-1]
            #current_state.print_state()

            print (current_state.getter())
            
            new_launched_nodes = list(launched_nodes)
            new_launched_nodes.append(adj_nodes[x])

            new_adj_nodes = list(adj_nodes)
            del new_adj_nodes[x]

            adj_list = find_adj_node(adj_nodes[x])

            #for node in adj_list:


            new_act_weight = act_weight + float(PESOS[adj_nodes[x]])

            next_states.extend(find_all_next_states(current_state, new_launched_nodes, new_adj_nodes, max_payload, new_act_weight))

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



def main():
    V, E, L, G = read_doc(DOC)
    print(PESOS)

    

    init = State(1,['VCM'])
    print (init.getter())

    node_list = find_adj_node('VCM')

    print (node_list)
    node_list = ['VS', 'VK1', 'VK2']
    all_states = find_all_next_states(init, init.get_element(), node_list, 22.8, 5)
    print (len(all_states))
    for a in all_states:
        a.print_state()

    print (init)

    print (State.compareState(all_states[2],all_states[4]))




if __name__ == "__main__":
    main()
