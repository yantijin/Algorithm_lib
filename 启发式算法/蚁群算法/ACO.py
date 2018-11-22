# coding = utf-8
import numpy as np
import matplotlib.pyplot as plt


def readCityInfo():
	data = []
	f = open("city.txt","r")
	for line in f.readlines():
		line.replace('\n', '', 1)
		data.append([float(line.split(" ")[0]),float(line.split(" ")[1])])
	return data



def calDistanceMatrix(data):
	size = len(data)
	mat = np.zeros((size,size))
	for i in range(size):
		for j in range(size):
			mat[i, j] = calEuclideanDis(data[i], data[j])
	return mat



def calEuclideanDis(a, b):
	size1 = len(a)
	size2 = len(b)
	if size1 != size2:
		print("输入维度不等，请检查")
		return 0
	dis = 0
	for i in range(size1):
		dis += (a[i] - b[i] )**2
	dis = np.sqrt(dis)
	return dis

	




if __name__ == "__main__":
	# 参数初始化
	antNum = 50
	alpha = 1 # 信息素的重要程度
	beta = 5 # 表征启发式因子的重要程度
	rho = 0.1 # 表示信息素挥发的系数
	gen = 0
	maxGen = 200 # 最大迭代次数
	Q = 100 # 信息素增加强度系数

	data = readCityInfo()
	cityNum = len(data)
	distanceMatrix = calDistanceMatrix(data)
	# print(len(distanceMatrix))
	eta = 1/distanceMatrix # 用距离的倒数表示启发式因子
	tau = np.ones((cityNum,cityNum)) # 信息素矩阵
	Tabu = np.zeros((antNum, cityNum)) # 存储每只蚂蚁的路径
	R_Best = np.zeros((maxGen, cityNum)) # 各代的最佳路线
	L_Best = np.inf * np.ones((maxGen, 1)) # 各代的路径长度


	while gen < maxGen:
		# 将m只蚂蚁分配到各个城市上
		randPos = []
		for i in range(int(np.ceil(antNum / cityNum))):
			a = np.arange(cityNum)
			np.random.shuffle(a)
			randPos = np.append(randPos, a)
		# print(randPos)
		Tabu[:, 0] = randPos[0: antNum]

		# m只蚂蚁按照概率函数选择自己所要走的路径
		for i in range(1,cityNum):
			for j in range(antNum):
				visited = Tabu[j, : i] # 已经访问过的城市
				wait4Visit = np.zeros((1,cityNum - i))
				flag = 0
				for k in range(cityNum):
					if k not in visited:
						wait4Visit[0, flag] = k
						flag += 1

				# 计算待选城市的概率分布
				P = []
				# print(type(visited[-1]))
				# print(type(wait4Visit[0,1]))
				for k in range(cityNum - i):
					P.append(tau[int(visited[-1]), int(wait4Visit[0, k])] ** alpha * eta[int(visited[-1]), int(wait4Visit[0, k])]** beta)

				P = P / sum(P)
				Psum = np.cumsum(P) # 概率累加之后的向量
				# print(Psum)
				temp = np.random.random()
				for l in range(len(Psum)):
					if Psum[l] >= temp:
						toVisit = wait4Visit[0, l]
						# print(toVisit)
						Tabu[j, i] = toVisit
						break
		if gen >= 1:
			Tabu[1, :] = R_Best[gen-1, :]

		# 记录本次迭代的最佳路线
		iterDistance = np.zeros((antNum,1))
		for i in range(antNum):
			R = Tabu[i, :]
			for j in range(cityNum - 1):
				iterDistance[i, 0] += distanceMatrix[int(R[j]), int(R[j+1])]
			iterDistance[i, 0] += distanceMatrix[int(R[0]), int(R[cityNum-1])]

		L_Best[gen, 0] = min(iterDistance)
		# print(iterDistance)
		index = list(iterDistance).index(L_Best[gen, 0])
		R_Best[gen, :] = Tabu[index, :]
		gen += 1
		print(gen)



		# 更新信息素矩阵
		DeltaTau = np.zeros((cityNum,cityNum))
		for i in range(antNum):
			for j in range(cityNum - 1):
				DeltaTau[int(Tabu[i, j]), int(Tabu[i, j+1])] += Q / iterDistance[i, 0]
			DeltaTau[int(Tabu[i, cityNum-1]), int(Tabu[i, 0])] += Q / iterDistance[i, 0]


		tau = (1 - rho) * tau + DeltaTau\


		# 清零禁忌表
		Tabu = np.zeros((antNum, cityNum))

	totalBest = min(L_Best)
	totalBestIndex = list(L_Best).index(totalBest)
	totalR_Best = R_Best[totalBestIndex, :]
	print(totalBest)
	print(totalR_Best)


	

	x = []
	y = []
	for i in range(len(totalR_Best)):
		x.append(data[int(totalR_Best[i])][0])
		y.append(data[int(totalR_Best[i])][1])
	x.append(x[0])
	y.append(y[0])

	plt.figure()
	plt.plot(x, y, 'b-')
	plt.plot(x, y, 'o')
	plt.figure()
	plt.plot(L_Best)

	plt.show()


























