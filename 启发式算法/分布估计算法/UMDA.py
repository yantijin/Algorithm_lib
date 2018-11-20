# coding = utf-8
'''
离散情形下的EDA
变量之间没有依赖
求f = \\sum x_i, i=1,2,3
x_i = {0,1}
'''
import numpy as np
import matplotlib.pyplot as plt

def initPop(popSize):
	pop = np.random.randint(0,2,(popSize, 3))
	return pop


def calFitness(pop):
	fitness = pop[:, 0] + pop[:, 1] +pop[:, 2]
	return fitness

def calProbability(pop, selNum):
	probability = np.zeros((3,1))
	for i in range(3):
		probability[i] = sum(pop[:,i]) / selNum
	return probability


def generateNewPop(proVector, popSize):
	pop = np.zeros((popSize,3))
	for i in range(popSize):
		for j in range(3):
			if np.random.random() > 1 - proVector[j]:
				pop[i, j] = 1
	return pop




if __name__ == "__main__":
	popSize = 10
	selNum = 5 # 从中选择的个体
	gen = 0
	maxGen = 10

	Best = []

	pop = initPop(popSize)
	while gen <= maxGen:
		fitness = calFitness(pop)
		Best.append(np.argmax(fitness))
		# 选出适应度较高的selNum个个体
		temp = np.argsort(fitness)
		temp1 = list(temp)
		temp1.reverse()
		# print(temp1)
		selPop = np.zeros((selNum,3))
		for i in range(selNum):
			selPop[i,:] = pop[temp1[i],:]

		# print(selPop)
		probability = calProbability(selPop, selNum)
		# print(probability)
		pop = generateNewPop(probability, popSize)
		gen += 1

	plt.plot(Best,'b-')
	plt.show()



