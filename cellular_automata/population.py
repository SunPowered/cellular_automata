"""
Generic Cellular Atomata Class and utils.
"""
import numpy as np
from itertools import islice

class Population(object):
	"""
		An object to represent a population of cells
	"""

	def __init__(self, N: int, rule_num: int = 30):
		"""
			Constructor.  

			:param N: 			The population size
			:param rule_num: 	The transform rule to apply
		"""
		self.rule_num = rule_num
		self.transform_map = self.transform_from_rule_number(rule_num)

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

		return res

	def transform_from_rule_number(self, rule_num):
		"""
		Create a hashmap for the numeric rule, ie Rule of 30
		"""

		assert rule < 256, "We can only handle rules to 256 (8 bit)"
		
		bit_array = np.unpackbits(np.array([[rule_num]], dtype=np.uint8))

		return dict(((k, v) for k, v in zip(range(7, -1, -1), bit_array)))

	def iter_window(self):
		"""
		Returns a generator that iterates through a size-3 window of the cells to create an integer state.  

		The window assumes continuous boundaries
		"""
		N = len(self.cells)

		for idx in range(N):
			lc = self.cells[i-1]
			cc = self.cells[i]
			rc = self.cells[(i+1) % N]

			yield int(''.join(lc, cc, rc), 2)

if __name__ == "__main__":
	# dirty testing
	pop = Population(5)

	for i in pop:
		print(i)