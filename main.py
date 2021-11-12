import localSearch
import argparse
import csv
import config

# python main.py rl11849.tsp -v
def getInput(f, CITIES):
	for _ in range(6):
		header = f.readline() # remove headers

	inp = f.readline().split()
	while len(inp) > 1 : # EOF
		N, x, y = map(lambda n : int(float(n)), inp)
		CITIES[N] = (x, y)
		inp = f.readline().split()

	if config.VERBOSE:
		print(f"Total number of cities : {len(CITIES)}") # DBG

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file', type=argparse.FileType('r'))
	parser.add_argument('-v', required=False, default=False, action='store_true', help='print out progress') # T/F flag
	parser.add_argument('-m', required=False, default=False, action='store_true', help='add flag to use 3-opt instead of 2-opt') # T/F flag
	parser.add_argument('-p', required=False, default=-1, type=int, help='population size (NOT USED IN CURRENT LOCAL SEARCH METHOD)') # num value flag
	parser.add_argument('-f', required=False, default=1000, type=int, help='limit the total number of fitness evaluations') # num value flag
	args = parser.parse_args()
	args_dic = vars(args)
	config.VERBOSE = args_dic['v']
	config.USE_THREE_OPT = args_dic['m']
	config.POP_SIZE = args_dic['p'] # -p option - population size (NOT USED IN CURRENT METHOD - LOCAL SEARCH)
	config.FITNESS_CNT = args_dic['f'] # -f option - fitness evaluation limit
	# print(args, type(args), args_dic) #ifdef DBG

	getInput(args.file, config.CITIES)

	# random path
	# from random import shuffle
	# path = [n for n in range(1, config.TOTAL_CITIES + 1)]
	# shuffle(path)

	# Initialize path with greedy method - Nearest Neighbor path
	path = localSearch.nearestNeighbors(goal=10000000)

	result_path = localSearch.run_localSearch(path, config.USE_THREE_OPT)

	# if config.FITNESS_CNT == 0:
	print(localSearch.getFitness(result_path, localSearch.dist))

	# save result path to csv
	with open('solution.csv', 'w') as f:
		write = csv.writer(f)
		for city in result_path:
			write.writerow([city])

	# else:
	# 	print("Error: FITNESS_CNT still left")

	# Draw result with matplotlib
	if config.VERBOSE:
		import visualize
		print("--End of program--")
		visualize.drawCities()
		visualize.drawPaths(path)