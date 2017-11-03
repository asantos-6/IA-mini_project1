#strategy.py
MAX = 999999

#uniform_cost: Uniform-cost algorithm/search strategy
#Arguments: List of states (nodes), weight dictionary, list of heuristic values for states
#Return: Expansion node
def uniform_cost(node_list, PESOS, HEURISTIC_VALUE):
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
#Arguments: State (node), heuristic value up until that state, average cost, weight dictionary
#Return: f value
def get_f_value(node, total_weight, average_cost, PESOS):
    weight_launched = 0

    for o in node.get_element():
        weight_launched += PESOS[o]

    g_cost = node.get_total_cost()
    h_value = average_cost* (total_weight - weight_launched)

    f_value = h_value + g_cost

    return f_value

#A_star: A* algorithm/search strategy
#Arguments: State list to search, weight dictionary, list of heuristic values for states
#Return: Expansion node
def A_star(node_list, PESOS, HEURISTIC_VALUE):
    minimo = MAX
    index = 0

    average_cost = HEURISTIC_VALUE[0]
    total_weight = 0
    for o in PESOS.values():
    	total_weight += o

    total_heuristic_value = average_cost*total_weight

    for x in range(0, len(node_list)):
        f_value = get_f_value(node_list[x], total_weight, HEURISTIC_VALUE[node_list[x].get_launch()-1], PESOS)
        if (minimo > f_value):
            minimo = f_value
            index = x
    expansion_node = node_list[index]
    del node_list[index]
    return expansion_node
