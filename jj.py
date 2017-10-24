import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import Counter

MAX = 999999
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
        self.Cost = []

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

    def get_cost(self):
        return self.Cost

    def get_total_cost(self):
        total_cost = 0
        for c in self.Cost:
            total_cost += c
        return total_cost


    def print_state(self):
        total_cost = 0
        for a in self.Cost:
            total_cost += a
        print ("state print:",self.Launch, self.Elements,"      path:", self.path, "    cost:", self.Cost, "    total_cost:", total_cost)
        return


    def compare(s,t):
        return Counter(s) == Counter(t)

    def compareState(a,b):
        if(a.Launch == b.Launch & compare(a.Elements,b.Elements)):
            return True
        else:
            return False

    def is_repeat(node_a, node_b):
        if node_a.Launch != node_b.Launch:
            return False
        if (len(node_a.Elements) != len(node_b.Elements)):
            return False

        if (set(node_a.Elements) == set(node_b.Elements)):
            return True

        return False

    def increment_launch(self):
        self.Launch += 1

    def save_path(self, past_path):
        self.path.append(past_path)

    def set_path(self, new_path):
        self.path = new_path

    def append_cost(self,cost):
        self.Cost = cost


    def actualize(self,previous_path):
        self.path = previous_path
        new_path = []
        i = 0
        for a in self.path:             #conta quantidades de elementos existentes em path. ou seja, numero de componentes ja lancados
            for b in a:
                i += 1 
        n = len(self.Elements) - i      #obtem se o numero de componentes que vai ser lancado neste launch
        if n == 0:
            previous_path.append([])
        if (n > 0):
            for x in range(i,len(self.Elements)):
                new_path.append(self.Elements[x])
            previous_path.append(new_path)

        self.path = previous_path

    def cost_is_higher(node_a, node_b):
        cost_a = 0
        cost_b = 0
        for c in node_a.Cost:
            cost_a += c
        for c in node_b.Cost:
            cost_b += c
        if cost_a > cost_b:
            return False
        else:
            return True

    





def read_doc(doc_name):

    Vertices = []                   #vetor de vertices do satelite
    Edges = []                      #vetor de edge dos satelite
    Weight = []                     #vetor de peso de componentes de satelite
    

    launch_info1 = []
    launch_info2 = []
    launch_info3 = []
    launch_info4 = []
    
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
                launch_info4.append((float(words[3]) + float(words[2] * float(words[4]))) / float(words[2]))
        line = f.readline()

    launch_datas.append(launch_info1)
    launch_datas.append(launch_info2)
    launch_datas.append(launch_info3)
    launch_datas.append(launch_info4)

    
    print (launch_datas)
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

def remove_launched_node(adj, launched):
    remove = []
    for x in range(0,len(adj)):
        for y in range(0, len(launched)):
            if adj[x] == launched[y]:
                remove.append(x)
                break
    
    print ("remove:", remove)
    for i in remove[::-1]:
        # print(i)
        # print (adj[i])
        # print (adj,launched)
        del adj[i]


def find_all_adj_nodes(launched_nodes):
    all_adj_nodes = []
    if (len(launched_nodes) < 1):           #se for primeiro lance, launch = 0, todos nos podem ser "adjacentes"
        for key in PESOS.keys():
            all_adj_nodes.append(key)
    else:
        for a in launched_nodes:
            addInexistentAdjNode(all_adj_nodes, find_adj_node(a))
    
    print (all_adj_nodes, launched_nodes)
    remove_launched_node(all_adj_nodes, launched_nodes)
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
        
def actualize_all_cost(state_list, previous_cost, launch_datas, Pesos):
    
    for a in state_list:
        total_cost = launch_datas[1][a.get_launch()]            #fixed cost
        path = a.get_path()
        state_cost = a.get_cost()
        if (len(path) > len(state_cost)):
            cost_list = list(previous_cost)
            if (len(path[-1]) == 0):
                cost_list.append(0)
                a.append_cost(cost_list)
            else:
                for e in path[-1]:
                    weight = Pesos[e]
                    total_cost += (launch_datas[2][a.get_launch()] * weight)
                cost_list.append(total_cost)
                a.append_cost(cost_list)

def remove_repeat_nodes(node_list):
    repeat_list = []
    for x in range(0,len(node_list)):
        
        for y in range(x+1,len(node_list)):
            if State.is_repeat(node_list[x], node_list[y]):
                repeat_list.append(x)
                break
    for i in repeat_list[::-1]:
        del node_list[i]


def successor(actual_state):
    childs = []
    all_elements = 0
    previous_path =  actual_state.get_path()            #fica com os caminhos feitos ate aqui
    for a in previous_path:
        all_elements += len(a)                          #faz somatorio de todos elementos ja lancados 
    previous_cost = actual_state.get_cost()             #fica com o custo utilizado para chegar atual estado
    
    if actual_state.get_launch() < len(launch_datas[0]):
        childs.append(actual_state)
        childs.extend(find_all_next_states(actual_state, actual_state.get_element(), find_all_adj_nodes(actual_state.get_element()), launch_datas[0][actual_state.get_launch()], 0))

        if (all_elements == 0):
            remove_repeat_nodes(childs)

        actualize_path(childs, previous_path)
        actualize_all_cost(childs,previous_cost, launch_datas, PESOS)


    
        add_launch(childs)


    return childs


def find_all_next_states(actual_state, launched_nodes, adj_nodes, max_payload, act_weight):
    next_states = []


    if (len(adj_nodes) > 0):
        
        new_elements = actual_state.get_element()
        for x in range(0, len(adj_nodes)):
            component_weight = PESOS[adj_nodes[x]]
            if ((act_weight+component_weight <= max_payload)):                  #so adiciona se nao exceder o max payload
                    new_elements = list(actual_state.get_element())
                    new_elements.append(adj_nodes[x])
                    new_elements1 = list(new_elements)
                    current_state = State(actual_state.get_launch(),new_elements1)
                    next_states.append(current_state)
                    del new_elements[-1]
                    new_launched_nodes = list(launched_nodes)
                    new_launched_nodes.append(adj_nodes[x])

                    new_adj_nodes = list(adj_nodes)
                    del new_adj_nodes[x]

                    adj_list = find_adj_node(adj_nodes[x])

                    new_act_weight = act_weight + float(PESOS[adj_nodes[x]])

                    if (len(adj_nodes) == len(PESOS)):                                          #estes dois linhas sao obras de arte, que corrige o erro dos nos adjacentes quando todos nos sao possiveis para aqueles so sao possiveis apos um componente
                        new_adj_nodes = find_all_adj_nodes(current_state.get_element())

                    addInexistenceState(next_states,find_all_next_states(current_state, new_launched_nodes, new_adj_nodes, max_payload, new_act_weight))  #so adiciona aqueles estados que ainda nao se encontram na lista e os estados possiveis(que apos todos lances ainda e possivel)

    return next_states

#find all adjacente nodes
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



def check_goal(state):
    if (len(state.get_element()) == len(PESOS)):
        return True
    else:
        return False


def exist_or_higher_cost(original_list, new_element):
    for a in original_list:
        if State.is_repeat(a,new_element):
            if State.cost_is_higher(a,new_element):
                return True
    return False



def add_new_or_low_cost_state(original_state, new_state):
    repeat_list = []
    for x in range(0, len(new_state)):
        if exist_or_higher_cost(original_state,new_state[x]):
            repeat_list.append(x)

    for i in repeat_list[::-1]:
        del new_state[i]

    original_state.extend(new_state)


'''
create a filter that remves impossible nodes
1 - node with max launch with incomplete satelite
'''
def state_filter(node_list):
    remove = []
    for x in range(0,len(node_list)):
        if (node_list[x].get_launch() == len(launch_datas[0])) and (len(node_list[x].get_element()) < len(PESOS)):
            remove.append(x)

    for i in remove[::-1]:
        del node_list[i]








def General_search(problem, strategy):
    open_list= []
    close_list = []

    open_list.append(problem)

    flag = 1
    while(flag):
        if not open_list:
            return False
        expansion_node = strategy(open_list)
        print ("expande node,", flag,":-------------", "lenght of open_list:", len(open_list))
        expansion_node.print_state()

        if (check_goal(expansion_node)):
            return expansion_node.get_path()
        else:


            child_nodes = successor(expansion_node)
            add_new_or_low_cost_state(open_list, child_nodes)

            state_filter(open_list)
            #open_list.extend(child_nodes)


        flag += 1

    print ("list:---------------------------")
    print ("list:---------------------------")
    print ("list:---------------------------")
    print (len(open_list))
    for a in open_list:
        a.print_state()

def uniform_cost(node_list):
    minimo = MAX
    index = MAX

    for x in range(0, len(node_list)):
        if (minimo > node_list[x].get_total_cost()):
            minimo = node_list[x].get_total_cost()
            index = x
    expansion_node = node_list[index]
    del node_list[index]
    return expansion_node


def main():
    V, E, L, G = read_doc(DOC)
    print(PESOS)

    init = State(0,[])
    # init = State(2,['V1','V2'])
    # init.save_path([['V1'],['V2']])
    # print ("gg:",find_all_adj_nodes(init.get_element()))
    # print (G['V2'])
    # childs = successor(init)
    # for a in childs:
    #     a.print_state()

    
    sol = General_search(init,uniform_cost)
    print ("solution:", sol)




if __name__ == "__main__":
    main()
