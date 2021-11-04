import visualize
import matplotlib.pyplot as plt
import math

def getInput(fname, CITIES):
	with open(fname, "r") as f:
		for _ in range(6):
			info = f.readline()
			# print(info) # DBG

		inp = f.readline().split()
		while len(inp) > 1 : # EOF
			N, x, y = map(lambda n : int(float(n)), inp)
			# print(N, x, y) # DBG
			CITIES[N] = (x, y)
			inp = f.readline().split()

		print(len(CITIES)) # DBG

def dist(city1, city2):
	X = 0
	Y = 1
	c1_pos = config.CITIES[city1]
	c2_pos = config.CITIES[city2]
	return math.sqrt((c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2)
# res = dist(1, 2)
# print(res)

def getFitness(path):
	fitness = 0
	for idx in range(1, config.TOTAL_CITIES):
		fitness += dist(path[idx], path[idx - 1])
	return fitness

def TwoOpt(path, i, j):
	new_path = path[:i]
	new_path += list(reversed(path[i:j+1]))
	new_path += path[j+1:]
	return new_path

# TODO - config 없애기
import config
import random

if __name__ == '__main__':
	random.seed(None)

	getInput("rl11849.tsp", config.CITIES)
	config.POP_SIZE = 100 # -p option
	# print(config.POP_SIZE) # DBG

	path = [n for n in range(1, config.TOTAL_CITIES + 1)]
	random.shuffle(path)

	gen = 0
	curFitness = getFitness(path)
	updated = False
	while True:
		updated = False
		gen += 1
		print(f'Gen {gen} : {curFitness}')

		for city1 in range(1, config.TOTAL_CITIES+1):
			for city2 in range(city1+1, config.TOTAL_CITIES+1):
				new_path = TwoOpt(path, city1, city2)
				newFitness = getFitness(new_path)
				if curFitness > newFitness:
					path = new_path
					curFitness = newFitness
					print(f"[Update] {city1} - {city2} better")
					updated = True
					break
				print(f"{city1} - {city2} worse")

			if updated:
				break
		else:
			break

		# if gen%100 == 0:
		# 	visualize.drawCities()
		# 	visualize.drawPaths(path)
		# 	plt.show()