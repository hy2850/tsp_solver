import visualize
import matplotlib.pyplot as plt
import math
import time

import argparse

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()

        if VERBOSE:
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

		if VERBOSE:
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

# def TwoOpt(path, city1, city2):
# 	i = path.index(city1)
# 	j = path.index(city2)
#
# 	new_path = path[:i]
# 	new_path += list(reversed(path[i:j+1]))
# 	new_path += path[j+1:]
# 	return new_path

def TwoOpt(path, i, j):
	new_path = path[:i]
	new_path += list(reversed(path[i:j+1]))
	new_path += path[j+1:]
	return new_path

# Choose 3 distinct segments A(i1, j1), B(i2, j2), C(i3, j3)
def ThreeOpt(path, i1, j1 ,i2, j2, i3, j3):
	new_paths = []

	# 1. identity - 1 case
	# new_paths.append(path)

	# 2. Two opt - 3 cases
	TwoOpt_paths = [TwoOpt(path, i1, j1), TwoOpt(path, i2, j2), TwoOpt(path, i3, j3)]
	new_paths += TwoOpt_paths

	# 3. Three opt - 4 cases
	ThreeOpt_paths = []
	ThreeOpt_paths.append(path[i2:j2+1] + path[j2+1:i3] + list(reversed(path[i3:j3+1])) + path[j3+1:] + path[:i1] + list(reversed(path[i1:j1+1])) + path[j1+1:i2]) # A'BC'
	ThreeOpt_paths.append(path[i3:j3+1] + path[j3+1:] + path[:i1] + list(reversed(path[i1:j1+1])) + path[j1+1:i2] + list(reversed(path[i2:j2+1])) + path[j2+1:i3]) # A'B'C
	ThreeOpt_paths.append(path[i1:j1+1] + path[j1+1:i2] + list(reversed(path[i2:j2+1])) + path[j2+1:i3] + list(reversed(path[i3:j3+1])) + path[j3+1:] + path[:i1]) # AB'C'
	ThreeOpt_paths.append(path[:i1] + list(reversed(path[i1:j1+1])) + path[j1+1:i2] + list(reversed(path[i2:j2+1])) + path[j2+1:i3] + list(reversed(path[i3:j3+1])) + path[j3+1:]) # A'B'C'
	new_paths += ThreeOpt_paths

	return new_paths


# O(N^2)
@timing
def nearestNeighbors(goal=10000000):
	if VERBOSE:
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

		if VERBOSE:
			print(now, end=" ") #ifdef DBG
			if len(available) % 50 == 0:
				print()

	return path

# search thoroughly from city 1
# No break after update
def run_localSearch(path):
	global curFitness
	for city1 in range(1, config.TOTAL_CITIES + 1):
		for city2 in range(city1 + 1, config.TOTAL_CITIES + 1):
			# if dist(city1, city2) > SEARCH_DIST_LIMIT:
			# 	if VERBOSE:
			# 		print(f"{city1} - {city2} too far - pass")
			# 	continue

			new_path = TwoOpt(path, city1, city2)
			# newFitness = getFitness(new_path, distSq)

			if config.FITNESS_CNT:
				newFitness = getFitness(new_path, dist)
				config.FITNESS_CNT -= 1

			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				if VERBOSE:
					print(f"[Update] {city1} - {city2} better - fitness {curFitness}")  # ifdef DBG
			# break

			if VERBOSE:
				print(f"{city1} - {city2} worse")  # ifdef DBG

# select first city randomly
# Break after update
def run_localSearch_random(path, use_ThreeOpt):
	global curFitness

	if use_ThreeOpt:
		while True:
			candidates = random.sample(range(0, config.TOTAL_CITIES), 6)
			candidates.sort()
			candidate_paths = ThreeOpt(path, *candidates)

			if config.FITNESS_CNT > len(candidate_paths):
				ThreeOpt_fitness = [getFitness(path, dist) for path in candidate_paths]
				config.FITNESS_CNT -= len(candidate_paths)
			else:
				config.FITNESS_CNT = 0
				return

			mix_path_idx = min(range(len(ThreeOpt_fitness)), key=ThreeOpt_fitness.__getitem__)
			new_path = candidate_paths[mix_path_idx]
			newFitness = ThreeOpt_fitness[mix_path_idx]
			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				if VERBOSE:
					print(f"[Update] better path config found - fitness {curFitness}")  # ifdef DBG
				break
			if VERBOSE:
				print("fail - re-try")

	else :
		while True:
			city1 = getRandomCity()
			city2 = -1
			while city1 >= city2:
				city2 = getRandomCity()

			new_path = TwoOpt(path, city1, city2)
			# newFitness = getFitness(new_path, distSq)
			newFitness = getFitness(new_path, dist)
			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				#if VERBOSE:
				print(f"[Update] {city1} - {city2} better - fitness {curFitness}")  # ifdef DBG

			if VERBOSE:
				print(f"{city1} - {city2} worse")  # ifdef DBG


# TODO - config 없애기
import config
import random

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', required=False, default=False, action='store_true', help='print out progress') # T/F flag
	parser.add_argument('-m', required=False, default=False, action='store_true', help='add flag to use 3-opt instead of 2-opt') # T/F flag
	parser.add_argument('-p', required=False, default=-1, type=int, help='population size (NOT USED IN LOCAL SEARCH)') # num value flag
	parser.add_argument('-f', required=False, default=100, type=int, help='limit the total number of fitness evaluations') # num value flag
	args = parser.parse_args()
	args_dic = vars(args)
	VERBOSE = args_dic['v']
	USE_THREE_OPT = args_dic['m']
	print(args, type(args), args_dic)

	random.seed(None)

	getInput("rl11849.tsp", config.CITIES)
	config.POP_SIZE = args_dic['p'] # -p option - population size (NOT USED IN CURRENT METHOD - LOCAL SEARCH)
	config.FITNESS_CNT = args_dic['f'] # -f option - fitness evaluation limit

	# path = [n for n in range(1, config.TOTAL_CITIES + 1)] # random path
	# random.shuffle(path)
	path = nearestNeighbors(goal=10000000) # Improvement 1) Nearest Neighbor path init (seeding?)

	gen = 0
	# curFitness = getFitness(path, distSq)
	if config.FITNESS_CNT:
		config.FITNESS_CNT -= 1
		curFitness = getFitness(path, dist)
	updated = False
	SEARCH_DIST_LIMIT = 7000 # two cities farther than this will be ignored
	while True:
		gen += 1
		# if VERBOSE:
		# print(f'Gen {gen} : {getFitness(path, distSq)}')
		# print(f'Gen {gen} : {getFitness(path, dist)}')

		run_localSearch_random(path, USE_THREE_OPT)

		if config.FITNESS_CNT == 0:
			# save path to csv with fitness
			pass

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