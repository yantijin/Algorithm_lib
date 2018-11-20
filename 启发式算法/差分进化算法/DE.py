# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt
'''
min f(x) = 20 + x1^2 + x2^2 - 10(cos2\\pi x1 + cos2\\pi x2)
x1,x2 \\in [-5,5]
'''

def initPopulation(popsize, vRange):
	pop = np.random.uniform(vRange[0], vRange[1], (popsize, 2))
	return pop

def calFitness(pop):
	fitness = 20 + pop[:,0]**2 + pop[:,1]**2 - 10 * (np.cos(2 * np.pi* pop[:,0])+ np.cos(2 * np.pi * pop[:,1]))
	return fitness


def mutateOperation(pop, F, strategy, indiPopBest = None):
	m, n = np.shape(pop)
	new_pop = np.zeros((m,n))
	if strategy == "rand/1" :
		for i in range(len(pop)):
			r1 = 0
			r2 = 0
			r3 = 0
			while r1 == i or r2 == i or r3 == i or r1 == r2 or r2 == r3 or r3 == r1:
				r1 = np.random.randint(0, m-1)
				r2 = np.random.randint(0, m-1)
				r3 = np.random.randint(0, m-1)

			for j in range(n):
				new_pop[i,j] = pop[r1, j] + F * (pop[r2, j] + pop[r3, j])
		return new_pop
	elif strategy == "rand/2":
		for i in range(len(pop)):
			r1 = 0
			r2 = 0
			r3 = 0
			r4 = 0
			r5 = 0
			while r1 == i or r2 ==i or r3 ==i or r4 == i or r5 ==i or r1 == r2 or r2 == r3 or r3 == r4 or r4 == r5 or r5 == r1 or r1 == r3 or r1 == r4 or r2 == r4 or r2 == r5 or r3 == r5:
				r1 = np.random.randint(0,m-1)
				r2 = np.random.randint(0,m-1)
				r3 = np.random.randint(0,m-1)
				r4 = np.random.randint(0,m-1)
				r5 = np.random.randint(0,m-1)
			for j in range(n):
				new_pop[i,j] = pop[r1, j] + F * (pop[r2, j] - pop[r3, j]) + F * (pop[r4, j] + pop[r5, j])
		return new_pop
	elif strategy == "best/1":
		if indiPopBest == None:
			print("参数缺失，请输入当前的全局最优")
			return 
		for i in  range(len(pop)):
			r1 = 0
			r2 = 0
			while r1 == i or r2 == i or r1 == r2:
				r1 = np.random.randint(0, m-1)
				r2 = np.random.randint(0, m-1)
			for j in range(n):
				new_pop[i, j] = indiPopBest[j] + F * (pop[r1, j] - pop[r2, j])
		return new_pop
	elif strategy == "best/2":
		if indiPopBest == None:
			print("参数缺失，请输入当前的全局最优")
			return 
		for i in range(len(pop)):
			r1 = 0
			r2 = 0
			r3 = 0
			r4 = 0
			while r1 == i or r2 == i or r3 == i or r4 == i or r1 ==r2 or r2 == r3 or r3 == r4 or r4 == r1 or r1 == r3 or r2 == r4:
				r1 = np.random.randint(0, m-1)
				r2 = np.random.randint(0, m-1)
				r3 = np.random.randint(0, m-1)
				r4 = np.random.randint(0, m-1)
			for j in range(n):
				new_pop[i, j] = indiPopBest[j] + F *(pop[r1, j] - pop[r2, j]) + F * (pop[r3, j] - pop[r4, j])
		return new_pop



def crossoverOperation(pop, new_pop, crossoverRate):
	m, n = np.shape(pop)
	croPop = np.zeros((m,n))
	for i in range(m):
		for j in range(n):
			r = np.random.random()
			if r < crossoverRate:
				croPop[i, j] = new_pop[i, j]
			else:
				croPop[i, j] = pop[i, j]
	return croPop



def selectOperation(pop, new_pop, fitness):
	m, n = np.shape(pop)
	new_fitness = calFitness(new_pop)
	for i in range(m):
		if new_fitness[i] < fitness[i]:
			for j in range(n):
				pop[i, j] = new_pop[i, j]
			fitness[i] = new_fitness[i]
	return pop, fitness




if __name__ == "__main__":
	# 初始化参数
	popsize = 20
	xRange = [-5, 5]
	F = 0.5
	CR = 0.8
	gen = 0
	maxGen = 1000

	# 最好适应度的值
	Best = []

	pop = initPopulation(popsize, xRange)
	fitness = calFitness(pop)

	while gen <= maxGen:
		new_pop = mutateOperation(pop, F, "rand/1")
		new_pop = crossoverOperation(pop, new_pop, CR)
		pop, fitness = selectOperation(pop, new_pop, fitness)
		Best.append(np.argmin(fitness))
		gen += 1

	print(min(Best))
	plt.plot(Best,'b-')
	plt.show()
