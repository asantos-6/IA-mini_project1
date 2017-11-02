


MAX = 999999
#uniform_cost: Uniformed cost algorithm/search strategy
#Arguments: List of states (nodes)
def uniform_cost(node_list, PESOS):
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
def get_f_value(node, total_heuristic_value, average_cost, PESOS):
    weight_launched = 0

    for o in node.get_element():
        weight_launched += PESOS[o]

    g_cost = node.get_total_cost()
    h_value = total_heuristic_value - (average_cost*weight_launched)

    f_value = h_value + g_cost

    return f_value

#A_star: A* algorithm/search strategy
#Arguments: State list to search
def A_star(node_list, PESOS):
    minimo = MAX
    index = 0

    average_cost = 2.3
    total_weight = 138.2
    total_heuristic_value = average_cost*total_weight

    #heuristic value for node = total_heuristic_value - (launched_weight * avereage_cost)

    for x in range(0, len(node_list)):
        f_value = get_f_value(node_list[x], total_heuristic_value, average_cost, PESOS)
        if (minimo > f_value):
            minimo = f_value
            index = x
    expansion_node = node_list[index]
    del node_list[index]
    return expansion_node


