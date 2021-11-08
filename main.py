import visualize
import matplotlib.pyplot as plt
import math
import time

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

INF = int(1e9)

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

		print(f"Total number of cities : {len(CITIES)}") # DBG

def dist(city1, city2):
	X = 0
	Y = 1
	c1_pos = config.CITIES[city1]
	c2_pos = config.CITIES[city2]
	return math.sqrt((c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2)

# Squared distance
def distSq(city1, city2):
	X = 0
	Y = 1
	c1_pos = config.CITIES[city1]
	c2_pos = config.CITIES[city2]
	return (c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2
# res = dist(1, 2)
# print(res)

def getRandomCity():
	return random.randint(1, config.TOTAL_CITIES)

def getFitness(path, distFunc):
	fitness = 0
	for idx in range(1, config.TOTAL_CITIES):
		fitness += distFunc(path[idx], path[idx - 1])
	return fitness

def TwoOpt(path, i, j):
	new_path = path[:i]
	new_path += list(reversed(path[i:j+1]))
	new_path += path[j+1:]
	return new_path

# O(N^2)
@timing
def nearestNeighbors(goal=10000000):
	print("Initialization of path : using Nearest Neighbor method - find closest city") #ifdef DBG
	print("New cities added : ")

	avg_needed = goal/config.TOTAL_CITIES # need this avg distance between two cities to achieve goal

	available = {n for n in range(1, config.TOTAL_CITIES+1)} # set
	path = []

	start = getRandomCity()
	path.append(start)
	available.remove(start)

	now = start
	while len(available) > 0:
		closest = -1 # next closest city to visit
		minDist = INF
		for nxtCity in available:
			d = distSq(now, nxtCity) # squared distance - reduce time for sqrt
			if d < minDist:
				closest = nxtCity
				minDist = d

				if minDist < avg_needed ** 2:
					break

		available.remove(closest)
		path.append(closest)
		now = closest

		print(now, end=" ") #ifdef DBG
		if len(available) % 50 == 0:
			print()

	return path


# TODO - config 없애기
import config
import random

if __name__ == '__main__':
	random.seed(None)

	getInput("rl11849.tsp", config.CITIES)
	config.POP_SIZE = 100 # -p option
	# print(config.POP_SIZE) # DBG

	# path = [n for n in range(1, config.TOTAL_CITIES + 1)] # random path
	# random.shuffle(path)
	path = nearestNeighbors(goal=5000000) # Improvement 1) Nearest Neighbor path init (seeding?)

	gen = 0
	# curFitness = getFitness(path, distSq)
	curFitness = getFitness(path, dist)
	updated = False
	SEARCH_DIST_LIMIT = 7000 # two cities farther than this will be ignored
	while True:
		gen += 1
		# print(f'Gen {gen} : {getFitness(path, distSq)}')
		print(f'Gen {gen} : {getFitness(path, dist)}')

		city1 = getRandomCity()
		for city2 in range(city1+1, config.TOTAL_CITIES+1):
			if dist(city1, city2) > SEARCH_DIST_LIMIT:
				print(f"{city1} - {city2} too far - pass")
				continue

			new_path = TwoOpt(path, city1, city2)
			# newFitness = getFitness(new_path, distSq)
			newFitness = getFitness(new_path, dist)
			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				print(f"[Update] {city1} - {city2} better") #ifdef DBG
				break
			print(f"{city1} - {city2} worse") #ifdef DBG


		if gen%5000 == 0:
			visualize.drawCities()
			visualize.drawPaths(path)
			plt.show()

		# fitness (total travel dist) history
		# Init : 86904764
		# Gen 10000 : 56074904 (1시간)
		# Gen 20000 : 38386621
		# Gen 30000 : 26448120 (3시간)
		# Gen 40000 : 18436226 (3시간)

	# verbose option -

# fitness 꾸준히 줄어들기는 하나, 너무 느리다. 3-opt 구현해볼까?