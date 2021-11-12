import config
import math
import time
import random

INF = int(1e9)

def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()

        if config.VERBOSE:
	        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap

def dist(city1, city2):
	X = 0
	Y = 1
	c1_pos = config.CITIES[city1]
	c2_pos = config.CITIES[city2]
	return math.sqrt((c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2)

def distSquared(city1, city2):
	X = 0
	Y = 1
	c1_pos = config.CITIES[city1]
	c2_pos = config.CITIES[city2]
	return (c1_pos[X] - c2_pos[X]) ** 2 + (c1_pos[Y] - c2_pos[Y]) ** 2

def getRandomCity(start = 1):
	return random.randint(start, config.TOTAL_CITIES)

def getFitness(path, distFunc):
	fitness = 0
	for idx in range(1, config.TOTAL_CITIES):
		fitness += distFunc(path[idx], path[idx - 1])
	return fitness

# Choose single segment (i,j) and re-order
def TwoOpt(path, i, j):
	new_path = path[:i]
	new_path += list(reversed(path[i:j+1]))
	new_path += path[j+1:]
	return new_path

# Choose 3 distinct segments A(i1, j1), B(i2, j2), C(i3, j3)
def ThreeOpt(path, i1, j1 ,i2, j2, i3, j3):
	new_paths = [] # an array of paths

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

	return new_paths # an array of paths

# O(N^2)
@timing
def nearestNeighbors(goal=10000000):
	if config.VERBOSE:
		print("Initialization of path : using Nearest Neighbor method - find closest city") #ifdef DBG
		print("New cities added : ")

	avg_needed = goal/config.TOTAL_CITIES # desired avg distance between two cities to achieve goal fitness

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
			d = distSquared(now, nxtCity) # squared distance - reduce time for sqrt
			if d < minDist:
				closest = nxtCity
				minDist = d

				if minDist < avg_needed ** 2:
					break

		available.remove(closest)
		path.append(closest)
		now = closest

		if config.VERBOSE:
			print(now, end=" ") #ifdef DBG
			if len(available) % 50 == 0:
				print()

	return path

# select first city randomly
# Break after update
def run_localSearch(path, use_ThreeOpt=False):
	random.seed(None)
	curFitness = getFitness(path, dist) # initial fitness

	if config.VERBOSE:
		print(f"Initialized to fitness {curFitness}")

	if use_ThreeOpt:
		while True:
			candidates = random.sample(range(0, config.TOTAL_CITIES), 6) # select 3 segments randomly
			candidates.sort()
			candidate_paths = ThreeOpt(path, *candidates)

			if config.FITNESS_CNT:
				ThreeOpt_fitness = [getFitness(path, dist) for path in candidate_paths]
				config.FITNESS_CNT -= 1
			else:
				return path

			min_path_idx = min(range(len(ThreeOpt_fitness)), key=ThreeOpt_fitness.__getitem__)
			new_path = candidate_paths[min_path_idx]
			newFitness = ThreeOpt_fitness[min_path_idx]

			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				if config.VERBOSE:
					print(f"[Update] better path config found - fitness {curFitness}")  # ifdef DBG
			if config.VERBOSE:
				print(f"Segment {candidates} worse")

	else :
		while True:
			city1 = getRandomCity()
			city2 = getRandomCity(city1+1)

			new_path = TwoOpt(path, city1, city2)
			if config.FITNESS_CNT:
				newFitness = getFitness(new_path, dist)
				config.FITNESS_CNT -= 1
			else:
				return path

			if curFitness > newFitness:
				path = new_path
				curFitness = newFitness
				if config.VERBOSE:
					print(f"[Update] {city1} - {city2} better - fitness {curFitness}")  # ifdef DBG

			if config.VERBOSE:
				print(f"{city1} - {city2} worse")  # ifdef DBG