def Expand(strategy, open_list):
    if strategy == "FIFO":
        return open_list[len(open_list)-1]
    else if strategy == "LIFO":
        return open_list[0]

def Check_Goal(x):
    if x.cost == 0:
        return x
    else:
        return False

def General_Search(problem, strategy):
    open_list = problem.graph[0]

    while True:
        if not open_list:
            return False

        expansion_node = Expand(strategy, open_list)
        for x in open_list:
            goal_check = Check_Goal(x)
            if len(goal_check) > 0:
                return goal_check
            else:
                childs = Create_Childs(problem.graph, problem.succ_function)
                for y in childs:
                    Update_Child(y, problem.g_function)
                    Add_Child(y, open_list, strategy)
                remove_parent(x, open_list)
