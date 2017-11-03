#General_search: General search algorithm (problem independent)
#Arguments: Problem definition, strategy to implement, weights dictionary, list of heuristic values for states
#Return: Goal state
def General_search(problem_1, strategy,PESOS,HEURISTIC_VALUE):
    open_list= []
    close_list = []
    open_list.append(problem_1.get_init())
    flag = 1

    successor = problem_1.get_successor()
    while(flag):
        if not open_list:
            return False
        expansion_node = strategy(open_list, PESOS, HEURISTIC_VALUE)
        if (problem_1.Check_Goal(expansion_node)):
            return expansion_node, flag
        else:
            child_nodes = successor(expansion_node)
            problem_1.Add_state(open_list, child_nodes)
        flag += 1
