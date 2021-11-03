from population import Population

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

import config
import random
if __name__ == '__main__':
	random.seed(None)

	getInput("rl11849.tsp", config.CITIES)
	config.POP_SIZE = 100 # -p option
	# print(config.POP_SIZE) # DBG

	pop = Population()

	gen = 0
	while True:
		pop.getPopulationFitness()

		gen += 1
		print(f'Gen {gen} : {pop.fitsum/config.POP_SIZE}')

		pop.selectParentTournament(1)

		pop.produceOffspring()

		pop.generationSelection(config.POP_SIZE)

		pop.printPop()
