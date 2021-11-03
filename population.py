from individual import Individual
import config
import random

class Population:
	def __init__(self):
		self.parentPop = []
		for _ in range(config.POP_SIZE):
			indiv = Individual()
			self.parentPop.append(indiv)
		self.childPop = []
		self.fitsum = 0

	# @args pop : POP_SIZE number of individuals (list of unique [1~TOTAL_CITIES] numbers with specific order)
	def getPopulationFitness(self):
		self.fitsum = 0
		for indiv in self.parentPop:
			indiv.getFitness()
			self.fitsum += indiv.fitness

	def selectParentTournament(self, K):
		self.childPop.clear()
		for i in range(config.POP_SIZE):
			tmp = []
			for j in range(K):
				tmp.append(self.parentPop[random.randint(0, config.POP_SIZE-1)])
			bestAmongK = min(tmp, key=lambda indiv: indiv.fitness)
			self.childPop.append(bestAmongK)

	def produceOffspring(self):
		for indiv in self.childPop:
			indiv.crossover()

		for indiv in self.childPop:
			indiv.mutation()

	# Gradual replacement
	def generationSelection(self, replaceCnt):
		self.parentPop.sort(key=lambda indiv: indiv.fitness, reverse=True)
		self.childPop.sort(key=lambda indiv: indiv.fitness)

		# Replace 'replaceCnt' individuals with lowest fitness from parent with same amount of best offsprings
		for idx in range(replaceCnt):
			self.parentPop[idx] = self.childPop[idx]

	def printPop(self):
		fitArr = []
		for child in self.parentPop:
			fitArr.append(child.fitness)
		fitArr.sort()
		print(fitArr)