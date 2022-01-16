import localSearch
import argparse
import csv
import config

def getInput(f, CITIES):
	inp = f.readline().split()
	while len(inp) : # EOF
		if inp[0].isnumeric() and len(inp) == 3:
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
	parser.add_argument('-g', required=False, default=0, type=int, help='fitness goal for nearest neighbor initialization') # num value flag
	parser.add_argument('-f', required=False, default=1000, type=int, help='limit the total number of fitness evaluations') # num value flag
	parser.add_argument('-p', required=False, default=-1, type=int, help='population size (NOT USED IN CURRENT LOCAL SEARCH METHOD)') # num value flag
	args = parser.parse_args()
	args_dic = vars(args)
	config.VERBOSE = args_dic['v']
	config.USE_THREE_OPT = args_dic['m']
	config.FITNESS_CNT = args_dic['f'] # -f option - fitness evaluation limit

	getInput(args.file, config.CITIES)
	config.TOTAL_CITIES = len(config.CITIES)

	# Path initialization
	# 1. random path
	# from random import shuffle
	# path = [n for n in range(1, config.TOTAL_CITIES + 1)]
	# shuffle(path)

	# 2. Nearest Neighbor (greedy)
	path = localSearch.nearestNeighbors(goal=args_dic['g'])

	# Run local search iteratively until stopping condition is met
	result_path = localSearch.run_localSearch(path, config.USE_THREE_OPT)

	# Result
	print(localSearch.getFitness(result_path, localSearch.dist))
	# save result path to csv
	with open('solution.csv', 'w', newline='') as f:
		write = csv.writer(f)
		for city in result_path:
			write.writerow([city])

	# VERBOSE : Draw result with matplotlib
	if config.VERBOSE:
		print("--End of program--")

		print("--Start visualization--")
		import visualize
		visualize.drawCities()
		visualize.drawPaths(path)
