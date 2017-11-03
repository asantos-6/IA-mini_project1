#Class Problem definition
class problem:
	def __init__(self, init_state, successor, path_cost, check, add_state):
		self.Init_state = init_state
		self.Successor = successor
		self.Path_cost = 0
		self.Check_Goal = check
		self.Add_state = add_state

	def get_init(self):
		return self.Init_state

	def get_successor(self):
		return self.Successor
