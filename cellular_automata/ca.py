"""
Generic Cellular Atomata Class and utils.
"""
import numpy as np
from itertools import islice

class Population(object):
	"""
		An object to represent a population of cells
	"""
	data_types = {
		1: ">i1",
		2: ">i1",
		3: ">i1",
		4: ">i2",
		5: ">i4",
		6: ">i8"
	}
	
	def __init__(self, N: int, rule_num: int=30):
		"""
			Constructor.  

			:param N: 			The population size
			:param rule_num: 	The transform rule to apply
		"""
		self.size = N
		self.rule_num = rule_num
		self.window_size = self.get_window_size(rule_num)
		self.transform_map = self.transform_from_rule_number()
		self._cells = self.empty_array(N)

		# init population
		self._cells[int(N/2)] = 1

	@property
	def cells(self):
		return self._cells

	def __iter__(self):
		return self._cells.__iter__()

	def __str__(self):
		return f"Population<N={len(self.cells)} Rule={self.rule_num}>"

	def empty_array(self, N):
		return np.zeros(N, dtype=np.uint8)

	def transform(self, transform_map=None):
		"""
			Using a hash map, transform_map, the population is iterated and a new population iteration is created and returned
		"""
		transform_map = transform_map or self.transform_map

		res = self.empty_array(len(self.cells))

		for idx, state in enumerate(self.iter_window()):
			res[idx] = transform_map[state]

		self._cells = res
		return res

	def transform_from_rule_number(self, rule_num=None, window_size=None):
		"""
		Create a hashmap for the numeric rule, ie Rule of 30
		"""
		rule_num = rule_num or self.rule_num
		window_size = window_size or self.window_size

		# assert rule_num < 256, "We can only handle rules to 256 (8 bit)"
		bit_array = np.unpackbits(np.array([[rule_num]], dtype=self.data_types[window_size]).view(np.uint8))

		return dict(((k, v) for k, v in zip(range(2**window_size - 1, -1, -1), bit_array)))

	def iter_window(self, window_size=3):
		"""
		Returns a generator that iterates through a size-3 window of the cells to create an integer state.  

		The window assumes continuous boundaries
		"""

		N = int((window_size - 1) / 2)  # This is the window offset

		for idx in range(self.size):
			# idx is the cell of interest, get the window of cells

			cells = [self.cells[(idx + offset) % self.size ] for offset in range(-1*N, window_size-N)]

			yield int(''.join(map(str, cells)), 2)

	def get_window_size(self, rule_num):

		l2 = np.log2(rule_num)

		if l2 / 8 < 1:
			return 3
		elif l2 / 16 < 1:
			return 4
		elif l2 / 32 < 1:
			return 5
		elif l2 / 64 < 1:
			return 6
		else:
			raise ValueError("Can't handle more than 64 bit transform vectors")

if __name__ == "__main__":
	# dirty testing
	pop = Population(5, 300)

	print(pop.window_size)

	#print(pop.transform_from_rule_number(30))
	#print(pop.transform_from_rule_number(300))