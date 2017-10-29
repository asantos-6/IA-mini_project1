

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
    def get_path_at(self, index):
        return self.path[index]

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
        self.path = past_path

    def save_cost(self, cost):
        self.Cost = cost       


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

    

