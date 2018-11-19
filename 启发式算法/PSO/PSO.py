# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt

'''
min f(x) = 20 + x1^2 + x2^2 - 10(cos2\\pi x1 + cos2\\pi x2)
x1,x2 \\in [-5,5]
'''

def calculateFitness(x):
	y = 20 + x[0]**2 + x[1]**2 - 10 * (np.cos(2 * np.pi * x[0]) + np.cos(2 * np.pi * x[1]))
	return y


def populationInitial(popsize):
	pop = 5 * np.random.uniform(-1, 1, (2, popsize))
	v = np.random.uniform(-1, 1, (2, popsize))
	return pop, v

if __name__ == "__main__":

	'''参数初始化'''

	# 权重参数
	w = 1.0
	c1 = 1.49445
	c2 = 1.49445
	# 速度和位置限制
	vRange = [-1, 1]
	posRange = [-5, 5]

	# 其他参数
	popsize = 20
	maxGen = 200 # 最大代数
	gen = 0 # 迭代的代数

	record = np.zeros(maxGen)

	pop, v = populationInitial(popsize)
	fitness = calculateFitness(pop)

	i = np.argmin(fitness) # 找到最好的个体的位置

	individualBest = pop
	globalBest = pop[:, i]
	fitnessIndiBest = fitness
	fitnessGlobalBest = fitness[i]

	

	while gen < maxGen:
		# 速度更新
		v = w * v + c1 * np.random.random() * (individualBest - pop) + c2 * np.random.random() * (globalBest.reshape(2,1) - pop)
		v[v > vRange[1]] = vRange[1]
		v[v < vRange[0]] = vRange[0]


		# 位置更新
		pop = pop + 0.5 * v
		pop[pop > posRange[1]] = posRange[1]  # 限制位置
		pop[pop < posRange[0]] = posRange[0]
		fitness = calculateFitness(pop)

		j = np.argmin(fitness)
		if fitness[j] < fitnessGlobalBest:
			fitnessGlobalBest = fitness[j]
			globalBest = pop[:, j]

		for i in range(popsize):
			if fitness[i] < fitnessIndiBest[i]:
				individualBest[:,i] = pop[:,i]
				fitnessIndiBest[i] = fitness[i]



		record[gen] = fitnessGlobalBest

		gen += 1

	print(fitnessGlobalBest)
	print(globalBest)
	plt.plot(record,'b-')
	plt.show()













