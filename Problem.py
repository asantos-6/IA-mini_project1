
class problem:
	def __init__(self, init_state, successor, path_cost):
		self.Init_state = init_state
		self.Successor = successor
		self.Path_cost = 0

	def get_init(self):
		return self.Init_state

	def get_successor(self):
		return self.Successor