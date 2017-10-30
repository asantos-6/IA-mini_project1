from jj import *

class Problem:
    def __init__(self, nodes, actions, graph):
        self.nodes = nodes
        self.actions = actions
        self.graph = graph

def Expand(strategy, open_list):
    if strategy == "FIFO":
        return open_list[len(open_list)-1]
    if strategy == "LIFO" or strategy == "uni":
        return open_list[0]

def Update_Child(state, launches):
    launch = launches[state.launch-1]
    state.cost = calc_cost(launch, state)
    return

def Add_Child(state, open_list, closed_list, strategy):
    insert = 1
    for n in closed_list:
        if n.launch == state.launch and set(elementID_list(n.elements)) == set(elementID_list(state.elements)):
            insert = 0
            break
    if insert:
        open_list.append(state)
        check_strategy(open_list, strategy)
    return

def check_strategy(open_list, strategy):
    if strategy == "uni":
        open_list.sort(key=lambda r: r.cost)
    return

def General_Search(problem, strategy):
    open_list = init_search(problem)
    closed_list = []
    for y in open_list:
        Update_Child(y, problem.actions)
    check_strategy(open_list, strategy)
    while True:
        if not open_list:
            return False
        #expansion_node = Expand(strategy, open_list)
        while open_list:
            goal_check = Check_Goal(problem.nodes, open_list[0])
            if goal_check:
                return goal_check
            else:
                childs = Create_Childs(open_list[0], problem)
                closed_list.append(open_list[0])
                for y in childs:
                    Update_Child(y, problem.actions)
                    Add_Child(y, open_list, closed_list, strategy)
                open_list.remove(open_list[0])
