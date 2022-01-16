import math
import random
from config import TOTAL_CITIES, CITIES, CROSSOVER_RATE, MUTATION_RATE

def dist(city1, city2):
	X = 0
	Y = 1
	c1_pos = CITIES[city1]
	c2_pos = CITIES[city2]
	return math.sqrt((c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2)
# res = dist(1, 2)
# print(res)

class Individual:
	def __init__(self, arr=None):
		if arr is not None:
			self.path = arr
		else:
			self.path = [n for n in range(1, TOTAL_CITIES + 1)]
			random.shuffle(self.path)
		self.fitness = self.getFitness()

	def getFitness(self):
		fitness = 0
		for idx in range(1, TOTAL_CITIES):
			fitness += dist(self.path[idx], self.path[idx - 1])
		return fitness

	# choose a point that divides array into two segments and swap the order of segment
	def crossover_single_point(self):
		if random.random() > CROSSOVER_RATE:
			return
		idx = random.randint(1, TOTAL_CITIES-2)
		self.path = self.path[idx:] + self.path[:idx]

	# Partially Mapped Crossover Operator
	def crossover_pmx(self, partner):
		# Step 1. Get two cut-points and swap the segment
		cut1 = random.randint(1, TOTAL_CITIES-2)
		cut2 = cut1
		while cut2 == cut1:
			cut2 = random.randint(1, TOTAL_CITIES-2)
		cut1, cut2 = min(cut1, cut2), max(cut1, cut2)

		# print(cut1, cut2) # ifdef DBG

		arr1 = [-1] * TOTAL_CITIES
		arr2 = [-1] * TOTAL_CITIES

		arr1[cut1:cut2+1], arr2[cut1:cut2+1] = tmp1, tmp2 = arr2[cut1:cut2+1], arr1[cut1:cut2+1]
		checkSet1 = set(tmp1)
		checkSet2 = set(tmp2)

		# Step 2. Inherit info from original parents, only non-conflicting ones
		for i in range(cut1):
			if self.path[i] not in checkSet1:
				arr1[i] = self.path[i]
				checkSet1.add(self.path[i])
			if partner.path[i] not in checkSet2:
				arr2[i] = partner.path[i]
				checkSet2.add(partner.path[i])

		for i in range(cut2+1, TOTAL_CITIES):
			if self.path[i] not in checkSet1:
				arr1[i] = self.path[i]
				checkSet1.add(self.path[i])
			if partner.path[i] not in checkSet2:
				arr2[i] = partner.path[i]
				checkSet2.add(partner.path[i])

		# Step 3. Fill the rest
		nxtCity1 = 1
		nxtCity2 = 1
		for i in range(TOTAL_CITIES):
			if arr1[i] == -1:
				while nxtCity1 in checkSet1:
					nxtCity1 += 1
				arr1[i] = nxtCity1
				checkSet1.add(nxtCity1)

			if arr2[i] == -1:
				while nxtCity2 in checkSet2:
					nxtCity2 += 1
				arr2[i] = nxtCity2
				checkSet2.add(nxtCity2)

		off1 = Individual(arr1)
		off2 = Individual(arr2)
		return off1, off2

	# swap order with other random city
	def mutation(self):
		for idx, city in enumerate(self.path):
			if random.random() > MUTATION_RATE:
				continue
			swap_idx = random.randint(0, TOTAL_CITIES-1)
			self.path[idx], self.path[swap_idx] = self.path[swap_idx], self.path[idx]

