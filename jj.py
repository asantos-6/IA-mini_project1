import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import Counter

DOC = "mir.txt"
G = nx.Graph()
PESOS = dict()
BUG = 0
launch_datas = []               #lista de lista onde contem as informacoes acerca de cada launch, cada lista contem max weight, fixed cost e variable cost

def increment():
    BUG += 1
    return

class State:

    def __init__(self, launch, elements_on_space):
        self.Launch = launch
        self.Elements = elements_on_space
        self.path = []
        self.Cost = 0

        return

    def getter(self):
        a = [self.Launch,self.Elements]
        return a

    def get_element(self):
        return self.Elements

    def get_launch(self):
        return self.Launch

    def get_path(self):
        return self.path

    def print_state(self):
        print ("state print:",self.Launch, self.Elements,"      path:", self.path)
        return

    def compare(s,t):
        return Counter(s) == Counter(t)

    def compareState(a,b):
        if(a.Launch == b.Launch & compare(a.Elements,b.Elements)):
            return True
        else:
            return False

    def increment_launch(self):
        self.Launch += 1

    def save_path(self, past_path):
        self.path.append(past_path)

    def set_path(self, new_path):
        self.path = new_path


    def actualize(self,previous_path):
        self.path = previous_path
        new_path = []
        i = 0
        for a in self.path:             #conta quantidades de elementos existentes em path. ou seja, numero de componentes ja lancados
            for b in a:
                i += 1 
        n = len(self.Elements) - i      #obtem se o numero de componentes que vai ser lancado neste launch
        print (self.Elements,self.path)
        print ("numero de elementos",n)    
        if n == 0:
            previous_path.append([])
            print ("count")
        if (n > 0):
            for x in range(i,len(self.Elements)):
                new_path.append(self.Elements[x])
            print ("old:",self.path, "    new:", new_path)
            previous_path.append(new_path)

        self.path = previous_path


def read_doc(doc_name):

    Vertices = []                   #vetor de vertices do satelite
    Edges = []                      #vetor de edge dos satelite
    Weight = []                     #vetor de peso de componentes de satelite
    

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
    
    for x in range(0,len(Vertices)):
        PESOS[Vertices[x]] = Weight[x]

    return Vertices, Edges, launch_datas, G


def isInList(list_a, b):
    for e in list_a:
        if State.compareState(e,b):
            return True
    return False

def isInList(list_a, element):
    for a in list_a:
        if (a == element):
            return True
    return False


def addInexistenceState(list_a, list_b):
    for s in list_b:
        if not isInList(list_a,s):
            list_a.append(s)



#add a inexistent node to the adjacente node list
#arguments: orinal list, list to add
def addInexistentAdjNode(original, additional):
    for a in additional:
        if not isInList(original, a):
            original.append(a)


def find_all_adj_nodes(launched_nodes):
    all_adj_nodes = []
    if (len(launched_nodes) < 1):
        for key in PESOS.keys():
            all_adj_nodes.append(key)
    else:
        for a in launched_nodes:
            addInexistentAdjNode(all_adj_nodes, find_adj_node(a))
    return all_adj_nodes


def add_launch(state_list):
    for a in state_list:
        a.increment_launch()

#actualiza o path de todos os estados que estao na lista
#vai primeiro meter o path para chegar ao estado pai e a seguir adiciona o path para chegar o estado atual
def actualize_path(state_list,previous_path):
    for a in state_list:
        aux = list(previous_path)
        a.actualize(aux)
        

def successor(actual_state):
    childs = []
    
    previous_path =  actual_state.get_path()
    childs.append(actual_state)
    childs.extend(find_all_next_states(actual_state, actual_state.get_element(), find_all_adj_nodes(actual_state.get_element()), launch_datas[actual_state.get_launch()][0], 0))

    print (actual_state, actual_state.get_element(), find_all_adj_nodes(actual_state.get_element()), launch_datas[actual_state.get_launch()][0], 0)
    add_launch(childs)
    print (actual_state.get_path())
    actualize_path(childs, previous_path)
    print (len(childs))
    for a in childs:
        a.print_state()

    actual_state.print_state()


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


def check_goal(state):
    if (len(state.get_element()) == len(PESOS)):
        return True
    else:
        return False

def General_search(problem, strategy):
    open_list= []
    close_list = []

    open_list.append(problem.init)

    while(True):
        if not open_list:
            return False
        expansion_node = strategy(open_list)
        if (check_goal(expansion_node)):
            return expansion_node.get_element()
        else:
            print ("nothing")

def main():
    V, E, L, G = read_doc(DOC)
    print(PESOS)

    init = State(0,['VCM'])
    init.save_path(['VCM'])
    successor(init)

    '''
    node_list = ['VS', 'VK1', 'VK2', 'VP', 'VPM', 'VSTM', 'VK', 'VDM']
    findAllLaunchStates(init,  init.get_element(), node_list,1,L)
    '''



if __name__ == "__main__":
    main()
