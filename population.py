from individual import Individual
import config
import random

class Population:
	def __init__(self):
		self.parentPop = [Individual() for _ in range(config.POP_SIZE)]
		self.matingPool = []
		self.childPop = []
		self.fitsum = 0

	# @args pop : POP_SIZE number of individuals (list of unique [1~TOTAL_CITIES] numbers with specific order)
	def getPopulationFitness(self):
		self.fitsum = 0
		for indiv in self.parentPop:
			indiv.getFitness()
			self.fitsum += indiv.fitness

	def selectParentTournament(self, K):
		self.matingPool.clear()
		for i in range(config.POP_SIZE):
			tmp = []
			for j in range(K):
				tmp.append(self.parentPop[random.randint(0, config.POP_SIZE-1)])
			bestAmongK = min(tmp, key=lambda indiv: indiv.fitness)
			self.matingPool.append(bestAmongK)

	def produceOffspring(self):
		self.childPop.clear()
		for i in range(config.POP_SIZE//2):
			parent1 = random.choice(self.parentPop)
			parent2 = random.choice(self.parentPop)
			off1, off2 = parent1.crossover_pmx(parent2)

			off1.mutation()
			off2.mutation()

			self.childPop.append(off1)
			self.childPop.append(off2)


	# Gradual replacement
	def generationSelection(self, replaceCnt):
		self.parentPop.sort(key=lambda indiv: indiv.fitness, reverse=True)
		self.childPop.sort(key=lambda indiv: indiv.fitness)

		# Replace 'replaceCnt' individuals with lowest fitness from parent with same amount of best offsprings
		for idx in range(replaceCnt):
			self.parentPop[idx] = self.childPop[idx]

	def printPop(self):
		self.parentPop.sort(key=lambda indiv: indiv.fitness)

		fitArr = []
		for child in self.parentPop:
			fitArr.append(child.fitness)
		print(fitArr)