# coding = utf-8
from random import randint
from random import random
from math import sin
from math import pi

# 学号： 1120153602
# 姓名： 闫媞锦
# 班级： 30041501
'''
f(x1,x2) = 21.5 + x1 sin(4 \\pi x1) + x2 sin(20 \\pi x2)
-3.0 \\leq x1 \\leq 12.1
4.1 \\leq x2 \\leq 5.8
pop size: 20
crossover rate = 0.25
mutation rate = 0.01
length of binary encoding:
	x1 18
	x2 15
	total length 18 + 15 =33
'''




def popInitialization(popNum, individualLength):
	# pop initialization
	pop = {}
	tempIndividual = ""
	for i in range(20):
		for j in range(33):
			tempIndividual += str(randint(0, 1))

		pop[i] = tempIndividual
		tempIndividual = ""
	return pop

def calEvaluation(popNum, pop):
	# adapability calculation
	evaluation = []
	for i in range(popNum):
		x1 = -3.0 + int(pop[i][: 18], 2) * (12.1 - (-3.0)) / (2 ** 18 - 1)
		x2 = 4.1 + int(pop[i][18 :], 2) * (5.8 - 4.1) / (2 ** 15 - 1)
		tempEval = 21.5 + x1 * sin(4 * pi * x1) + x2 * sin(20 * pi * x2)
		evaluation.append(tempEval)
	return evaluation

def selOperation(evaluation, popNum, pop):
	# selection operation
	# Calculate the selection rate for each individual
	selectionRate = []
	sumEvalutaion = sum(evaluation)
	for evalu in evaluation:
		selectionRate.append(evalu / sumEvalutaion)

	# Calculate the random reference for new population
	selectRef = []
	new_pop = pop
	for i in range(popNum):
		selectRef.append(random())


	for j in range(len(selectRef)):
		for k in range(len(selectionRate)):
			if selectRef[j] < selectionRate[k]:
				new_pop[j] = pop[k]
	return new_pop

def croOperation(popNum, new_pop):
	# Crossover operation
	# find the individuals for crossover operation
	tempCro = []
	selPop = {}
	for j in range(popNum):
		tempCro.append(random())


	selCro = {}
	for i in range(popNum):
		if tempCro[i] < croRate:
			selCro[i] = new_pop[i]

	croNum = list(selCro.keys())
	if len(croNum) % 2 ==1:
		croNum.append(croNum[0])

	for i in range(int(len(croNum)/2)):
		temp = randint(0, 31)
		tempPop1 = new_pop[croNum[2 * i]][: temp] + new_pop[croNum[2 * i + 1]][temp :]
		tempPop2 = new_pop[croNum[2 * i + 1]][: temp] + new_pop[croNum[2 * i]][temp :]
		new_pop[croNum[2 * i]] = tempPop1
		new_pop[croNum[2 * i + 1]] = tempPop2
	return new_pop

def mutOperation(popNum, individualLength, new_pop):
	# Mutaion operation
	for i in range(popNum):
		for j in range(individualLength):
			if random() < mutRate:
				mutationPlace = str(1-int(new_pop[i][j]))
				tempIndividual = new_pop[i][:j] + mutationPlace + new_pop[i][j+1 :]
				new_pop[i] = tempIndividual
	return new_pop


if __name__ == "__main__":
	# parameters settings
	popNum = 20
	croRate = 0.25
	mutRate = 0.01
	individualLength = 33
	pop = popInitialization(popNum, individualLength)
	evaluation = calEvaluation(popNum, pop)
	maxEvaluation = max(evaluation)
	maxEvaluationIndex = evaluation.index(maxEvaluation)
	for k in range(1000):
		new_pop = selOperation(evaluation, popNum, pop)
		new_pop = croOperation(popNum, new_pop)
		new_pop = mutOperation(popNum, individualLength, new_pop)
		pop = new_pop
		evaluation = calEvaluation(popNum, pop)
		if max(evaluation) > maxEvaluation:
			maxEvaluation = max(evaluation)
			maxEvaluationIndex = evaluation.index(maxEvaluation)

	print(maxEvaluation)
	print(maxEvaluationIndex)





