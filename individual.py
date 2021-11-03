import math
import random
from config import TOTAL_CITIES, CITIES, CROSSOVER_RATE, MUTATION_RATE

class Individual:
	def __init__(self):
		self.cities = [n for n in range(1, TOTAL_CITIES + 1)]
		random.shuffle(self.cities)
		self.fitness = self.getFitness()

	def dist(self, city1, city2):
		X = 0
		Y = 1
		c1_pos = CITIES[city1]
		c2_pos = CITIES[city2]
		return math.sqrt((c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2)
	# res = dist(1, 2)
	# print(res)

	def getFitness(self):
		fitness = 0
		for idx in range(1, TOTAL_CITIES):
			fitness += self.dist(self.cities[idx], self.cities[idx - 1])
		return fitness

	# choose a point that divides array into two segments and swap the order of segment
	def crossover(self):
		if random.random() > CROSSOVER_RATE:
			return
		idx = random.randint(1, TOTAL_CITIES-2)
		self.cities = self.cities[idx:] + self.cities[:idx]

	# swap order with other random city
	def mutation(self):
		for idx, city in enumerate(self.cities):
			if random.random() > MUTATION_RATE:
				continue
			swap_idx = random.randint(0, TOTAL_CITIES-1)
			self.cities[idx], self.cities[swap_idx] = self.cities[swap_idx], self.cities[idx]

