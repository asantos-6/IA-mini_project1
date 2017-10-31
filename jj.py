import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import Counter
import copy
import scipy as sp
import numpy as np
from State import State
from operator import itemgetter

MAX = 999999
MAX_PRICE = 0
INDEX = 0
DOC = "mir.txt"
G = nx.Graph()
PESOS = dict()
BUG = 0
launch_datas = []               #Matrix containing launch informations
VERTICES = []
V = []


def get_launch_data(data):
    data.sort(key = lambda row: row[0])
    launch_info0 = []               #List with each launch date
    launch_info1 = []               #List with each launch max payload
    launch_info2 = []               #List with each launch fixed cost
    launch_info3 = []               #List with each launc variable cost
    launch_info4 = []               #List with each launch cost per unit weight

    for d in data:
        launch_info0.append(d[0])
        launch_info1.append(d[1])
        launch_info2.append(d[2])
        launch_info3.append(d[3])
        launch_info4.append(d[4])

    #The information of the launches is stored in a list called launch_datas
    launch_datas.append(launch_info1)
    launch_datas.append(launch_info2)
    launch_datas.append(launch_info3)
    launch_datas.append(launch_info4)
    launch_datas.append(launch_info0)


#read_doc: Reads the input document and returns the read data
#Arguments: text file to be read
def read_doc(doc_name):

    Vertices = []                   #Vertices list
    Edges = []                      #Satelite edges
    Weight = []                     #Component weights list



def read_doc(doc_name):

    Vertices = []                   #vetor de vertices do satelite
    Edges = []                      #vetor de edge dos satelite
    Weight = []                     #vetor de peso de componentes de satelite
    dates = []
    f = open(doc_name)
    line = f.readline()
    while line:
        line = line.replace("\n","")
        words = line.split(" ")
        if(words[0] != ""):
            #Reading the vertices from the input file
            if(words[0][0] == "V"):
                G.add_node(words[0])
                VERTICES.append(words[0])
                Weight.append(float(words[1]))
            #Reading the edges from the input file
            if(words[0][0] == "E"):
                edge_pair = []
                edge = (words[1], words[2])
                edge_pair.append(words[1])
                edge_pair.append(words[2])
                G.add_edge(*edge)
                Edges.append(edge_pair)
            #Reading the launches from the input file
            if(words[0][0] == 'L'):
                date = []
                date.append(int(words[1][4:8] + words[1][2:4] + words[1][0:2]))
                date.append(float(words[2]))
                date.append(float(words[3]))
                date.append(float(words[4]))
                date.append(((float(words[3]) + float(words[2]) * float(words[4]))) / float(words[2]))
                dates.append(date)

        line = f.readline()

    get_launch_data(dates)


    print (launch_datas)
    for x in range(0,len( VERTICES)):
        PESOS[VERTICES[x]] = Weight[x]

    return  VERTICES, Edges, launch_datas, G

#isInList: Checks if a state/element is in a list
#Arguments: list to check, state/element to check if it's in the list
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

#combinations: Finds all combinations (??)
#Arguments: (??)
def combinations(target,data):
    result = []
    for i in range(len(data)):
        new_target = copy.copy(target)
        new_data = copy.copy(data)
        new_target.append(data[i])
        new_data = data[i+1:]
        result.append(new_target)
        result.extend(combinations(new_target,new_data))
    return result

#addInexistenceState: Adds an inexistent state from one list to another list
#Arguments: list to add elements, list from which the elements will be added to the other
def addInexistenceState(list_a, list_b):
    for s in list_b:
        if not isInList(list_a,s):
            list_a.append(s)

#addInexistentAdjNode: Adds an inexistent node to the adjacent node list
#Arguments: original list, list to add
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
    for i in remove[::-1]:
        del adj[i]


#find_all_adj_nodes: Finds all the adjacent nodes to a set of nodes
#Arguments: Set of nodes to check adjacent node
def find_all_adj_nodes(launched_nodes):
    all_adj_nodes = []
    if (len(launched_nodes) < 1):           #se for primeiro lance, launch = 0, todos nos podem ser "adjacentes"
        for key in PESOS.keys():
            all_adj_nodes.append(key)
    else:
        for a in launched_nodes:
            addInexistentAdjNode(all_adj_nodes, find_adj_node(a))
    remove_launched_node(all_adj_nodes, launched_nodes)
    return all_adj_nodes


#add_launch: Increments the launch index for each state in a list of states
#Arguments: List of states
def add_launch(state_list):
    for a in state_list:
        a.increment_launch()

#actualize_path: Updates the path of every state that is in state_list. First it finds the previous path up to the father node
#and then it adds the path from the father node to cureent (child) node
#Arguments: List of states to update path, previous path
def actualize_path(state_list,previous_path):
    for a in state_list:
        aux = list(previous_path)
        a.actualize(aux)

#actualize_all_cost: Updates all state costs regarding the last state change
#Arguments: List of states, previous cost, launch information, weights dictionary
def actualize_all_cost(state_list, previous_cost, launch_datas, Pesos):
    for a in state_list:
        total_cost = launch_datas[1][a.get_launch()]       #fixed cost
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


#remove_repeat_nodes: Removes repeated nodes from a list of nodes
#Arguments: List from which to remove the repeated nodes
def remove_repeat_nodes(node_list):
    repeat_list = []
    for x in range(0,len(node_list)):

        for y in range(x+1,len(node_list)):
            if State.is_repeat(node_list[x], node_list[y]):
                repeat_list.append(x)
                break
    for i in repeat_list[::-1]:
        del node_list[i]


#is_same_list: Compares the components of two lists
#Arguments: Lists to compare
def is_same_list(list_a, list_b):
    if set(list_a) == set(list_b):
        return True
    else:
        return False

#state_cost_filter: Filters out the states whith the same number of launches and with the same components already in space,
#leaving just the state with less cost
#Arguments: List of states(nodes) to filter out
def state_cost_filter(node_list):

    init = 0
    min_index = init
    min_value = node_list[init].get_total_cost()
    remove_list = []

    bit = 1
    while (bit):
        init += 1

        for y in range(init, len(node_list)):
            if (len(node_list[init].get_element()) == len(node_list[y].get_element())) and (is_same_list(node_list[init].get_element(), node_list[y].get_element())):
                if node_list[y].get_total_cost() < min_value:
                    min_value = node_list[y].get_total_cost()
                    min_index = y
                remove_list.append(y)

        for i in remove_list[::-1]:
            if i != min_index:
                del node_list[i]
        remove_list = []

        if (init + 1) >= len(node_list):
            break
        min_value = node_list[init].get_total_cost()
        min_index = init


#remove_exceed_weight: Removes all the combinations that exceed the max payload of a launch
#Arguments: List of nodes, max payload of a launch
def remove_exceed_weight(node_list, max_payload):
    remove = []

    for x in range(len(node_list)):
        total_weight = 0
        for e in node_list[x]:
            total_weight += PESOS[e]
        if total_weight > max_payload:
            remove.append(x)

    for x in remove[::-1]:
        del node_list[x]

#remove_not_connected: Deletes situations in ehich the nodes are not all connected amongst themselves in station the graph
#Arguments: List of nodes, already launched elements
def remove_not_connected(node_list, launched_elements):
    remove = []

    for x in range(0, len(node_list)):
        if len(node_list[x]) >= 2:
            all_elements = list(launched_elements)
            all_elements.extend(node_list[x])
            A = nx.adjacency_matrix(G,all_elements)
            for y in A.todense():
                #print (A.todense(), node_list[x])
                if not np.any(y):
                    remove.append(x)
                    #print ("XXXX:", x)
                    break

    for x in remove[::-1]:
        del node_list[x]

#find_all_next_states_by_combination: Given a state as an input, this function returns every possible state that succeeds it by combinations
#Arguments: State from which to find the succeeding states, max payload
def find_all_next_states_by_combination(state, max_payload):
    target = []
    childs = []
    all_elements = list(VERTICES)
    launched_elements = list(state.get_element())

    #Checks which elements are already there or not
    for e in launched_elements:
        all_elements.remove(e)

    #Finds the combinations of a given state
    result = combinations(target,all_elements)

    #Removes extra states
    remove_exceed_weight(result, max_payload)
    remove_not_connected(result, launched_elements)

    #For each element in result, creates all the new states with the updated element list for each state
    for e in result:
        previous_launched = list(state.get_element())

        previous_launched.extend(e)
        new_launched = list(previous_launched)

        new_state = State(state.get_launch(),new_launched)

        childs.append(new_state)

    return  childs

#successor: Finds the next states of a given state by two means possible: combinations or recursive fucntion
#Arguments: State from which to find the succeeding states
def successor(actual_state):
    childs = []
    all_elements = 0
    previous_path = actual_state.get_path()            #Stores preceeding path
    for a in previous_path:
        all_elements += len(a)                          #Sums the amount of elements already launched
    previous_cost = actual_state.get_cost()             #Stores the previous cost from current state to update the next states

    if actual_state.get_launch() < len(launch_datas[0]):
        childs.append(actual_state)

        #If the max payload exceeds a certain weight threshold, find the next states by combinations
        if (launch_datas[0][actual_state.get_launch()] > 40):
            childs.extend(find_all_next_states_by_combination(actual_state, launch_datas[0][actual_state.get_launch()]))
        #Else, fidnthe next states calling the recursive function designed for this purpose
        else:
            childs.extend(find_all_next_states(actual_state, actual_state.get_element(), find_all_adj_nodes(actual_state.get_element()), launch_datas[0][actual_state.get_launch()], 0))

        if (all_elements == 0):
            remove_repeat_nodes(childs)

        #Update path and cost of the staes found
        actualize_path(childs, previous_path)
        actualize_all_cost(childs,previous_cost, launch_datas, PESOS)

        add_launch(childs)

    #Filter the states found
    state_filter(childs)

    return childs


#new_nodes: This function finds the unlaunched new adjacent nodes
#Arguments:  list of already launched nodes,list of new adjacent nodes of the new launched node
def new_nodes(launched_nodes, new):
    repeat_list = []

    for x in range(0, len(new)):
        for y in range(0, len(launched_nodes)):
            if new[x] == launched_nodes[y]:
                repeat_list.append(x)

    for x in repeat_list[::-1]:
        del new[x]
    return new

#find_all_next_states: Given a state as an input, this function returns every possible state that succeeds it recursively
#Arguments: State from which to find the succeeding states, already launched nodes, adjacent nodes, max payload, current weight
def find_all_next_states(actual_state, launched_nodes, adj_nodes, max_payload, act_weight):
    next_states = []

    if (len(adj_nodes) > 0):
        previous_elements = actual_state.get_element()
        for x in range(0, len(adj_nodes)):
            component_weight = PESOS[adj_nodes[x]]
            if ((act_weight+component_weight <= max_payload)):       #It only adss if it doesn't exceed the max payload
                previous_launched = list(launched_nodes)
                new_launched = list(previous_launched)
                new_launched.append(adj_nodes[x])
                new_state = State(actual_state.get_launch(),new_launched)
                next_states.append(new_state)

                new_adj_nodes = list(adj_nodes)
                del new_adj_nodes[x]

                adj_list = find_adj_node(adj_nodes[x])

                new_adj_nodes.extend(new_nodes(new_launched, adj_list))
                new_act_weight = act_weight + float(PESOS[adj_nodes[x]])

                if (len(adj_nodes) == len(PESOS)):   #Não sei o q diga aqui XIA                #estes dois linhas sao obras de arte, que corrige o erro dos nos adjacentes quando todos nos sao possiveis para aqueles so sao possiveis apos um componente
                    new_adj_nodes = find_all_adj_nodes(new_state.get_element())
                addInexistenceState(next_states,find_all_next_states(new_state, new_state.get_element(), new_adj_nodes, max_payload, new_act_weight))  #Only adds those states that are still not accounted for

    return next_states


#find_adj_node: Finds all adjacent nodes given a node
#Arguments: State (node)
def find_adj_node(node):
    node_key = G[node]
    node_list = []
    for key in node_key.keys():
        node_list.append(key)
    return node_list

#check_goal: Goal checking function
#Arguments: State to check wheter if it's a goal state or not
def check_goal(state):
    if (len(state.get_element()) == len(PESOS)):
        return True
    else:
        return False

#exist_or_higher_cost: Checks wether a state already exists or has higher cost than the ones already there
#Arguments: List of original states, state to check
def exist_or_higher_cost(original_list, new_element):
    for a in original_list:
        if State.is_repeat(a,new_element):
            if State.cost_is_higher(a,new_element):
                return True
    return False

#add_new_or_low_cost_state: Replaces a state if the algorithm finds a same state with less cost
#Arguments: List of original states, list of new states
def add_new_or_low_cost_state(original_states, new_states):
    repeat_list = []
    for x in range(0, len(new_states)):
        if exist_or_higher_cost(original_states,new_states[x]):
            repeat_list.append(x)

    for i in repeat_list[::-1]:
        del new_states[i]

    original_states.extend(new_states)


'''
create a filter that remves impossible nodes
1 - node with max launch with incomplete satelite
'''
#state_filter: Filters out impossible states. Ex.: State that exhausted all the launches but still hasn't all elements in the outer space
#Arguments: List of nodes to filter
def state_filter(node_list):
    remove = []
    elements = []

    #Removes states that already reach all launches, but still didn't have all components in the outer space
    for x in range(0,len(node_list)):
        if (node_list[x].get_launch() == len(launch_datas[0])) and (len(node_list[x].get_element()) < len(PESOS)): #remove all incomplete launch
            remove.append(x)
            continue

    for i in remove[::-1]:
        del node_list[i]

    #Removes all the states that have the same elements, independtly of the order of which they were sent or built
    if (len(node_list) > 0) and (node_list[0].get_launch() >= 2):
        index = 0
        while(True):
            remove = []
            for y in range(index+1, len(node_list)):
                if (len(node_list[index].get_path_at(node_list[index].get_launch()-1)) +len(node_list[index].get_path_at(node_list[y].get_launch()-1)) > 0):
                    if  (is_same_list(node_list[index].get_path_at(node_list[index].get_launch()-1), node_list[y].get_path_at(node_list[y].get_launch()-1))):
                        remove.append(y)
            for i in remove[::-1]:
                del node_list[i]

            index += 1
            if (index + 1) >= len(node_list):
                break

#uniform_cost: Search strategy. Selects the state with less cost for expansion
#Arguments: List of states (nodes)
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

#get_f_value: Returns the f value of a given state
#Arguments: State (node), heuristic value up until that state, average cost
def get_f_value(node, total_heuristic_value, average_cost):
    weight_launched = 0

    for o in node.get_element():
        weight_launched += PESOS[o]

    g_cost = node.get_total_cost()
    h_value = total_heuristic_value - (average_cost*weight_launched)

    f_value = h_value + g_cost

    return f_value

#A_star: A* algorithm
#Arguments: State list to search
def A_star(node_list):
    minimo = MAX
    index = 0

    average_cost = 2.3
    total_weight = 138.2
    total_heuristic_value = average_cost*total_weight

    #heuristic value for node = total_heuristic_value - (launched_weight * avereage_cost)

    for x in range(0, len(node_list)):
        heuristic_value = get_f_value(node_list[x], total_heuristic_value, average_cost)
        if (minimo > heuristic_value):
            minimo = heuristic_value
            index = x
    expansion_node = node_list[index]
    del node_list[index]
    return expansion_node

#General_search: General search algorithm (problem independent)
#Arguments: Problem definition, strategy to implement
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
            #print ("node number:", flag)
            add_new_or_low_cost_state(open_list, child_nodes)

            #state_filter(open_list)
            #open_list.extend(child_nodes)


        flag += 1

    print (len(open_list))
    for a in open_list:
        a.print_state()

def main():
    V, E, L, G = read_doc(DOC)
    print(PESOS)
    MAX_PRICE = 0

    for a in range(0,len(launch_datas[3])):
        if MAX_PRICE < launch_datas[3][a]:
            MAX_PRICE = launch_datas[3][a]
            INDEX = a


    # init = State(9,['VK1','VCM'])
    # init.save_path([[], [], [], [], [],[],[],['VK1'],['VCM']])

    # init.save_cost([0, 0, 0, 0, 0,0,0,57.24,52.4])
    # init.print_state()
    # childs = successor(init)

    # print ("len:", len(childs))
    # for a in childs:
    #     a.print_state()

    #     if (len(a.get_element()) == 9):
    #         print ("------------------")
    #         a.print_state
    #         print ("------------------")


    init = State(0,[])
    #init.save_path([[], []])
    #init.save_cost([0, 0])

    sol = General_search(init,A_star)
    #sol = General_search(init,uniform_cost)
    print ("solution:", sol)

if __name__ == "__main__":
    main()
