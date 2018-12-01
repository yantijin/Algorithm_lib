from math import sqrt
import numpy as np
import csv
import matplotlib.pyplot as plt


from dbscanner import DBScanner
import re, csv, sys


def readData(filepath):
	data = []
	with open(filepath,'r') as file_obj:
		csv_reader = csv.reader(file_obj)
		for row in csv_reader:
			if len(row) < 2:
				print("数据有误，请检查")
				return
			else:
				data1 = []
				for l in range(len(row)-1):
					data1.append(float(row[l]))
				data.append(data1)
	return data

# 计算两个向量之间的距离
def calDistance(x1, x2):
	a1 = len(x1)
	a2 = len(x2)
	if a1 != a2:
		print("两个向量维度不等，请检查！")
		return

	distance = 0
	for i in range(a1):
		distance += (x1[i] - x2[i])**2
	distance = sqrt(distance)

	return distance

# 计算距离矩阵
def calDistanceMatrix(data):
	lenData = len(data)
	distanceMatrix = np.zeros((lenData,lenData))
	for i in range(lenData):
		for j in range(lenData):
			distanceMatrix[i,j] = calDistance(data[i], data[j])
	distanceMatrix = np.mat(distanceMatrix) + np.mat(distanceMatrix).T
	# print(distanceMatrix[25,:])
	return distanceMatrix


# 获取每个点到距离他第k近的点的距离，得到一个从大到小的列表
def getKdistance(k, distanceMatrix):
	distanceList = []
	for i in range(len(distanceMatrix)):
		l = distanceMatrix[i,:]
		l.sort()
		# 因为第一个点肯定是0，是自己，所以坐标点是[0,k]，是算上自己之后应该是第k+1个点
		tempDis = l[0,k]
		distanceList.append(tempDis)
	# print(distanceList)

	distanceList.sort()
	distanceList.reverse()
	return distanceList

# 根据kdist计算候选的eps
# l是算此点和往前第几个点之间的斜率
# slope设定的临界斜率值，如果小于此值就加入到epsCandidate中
def calEpsCandidate(distanceList, l, slope):
	lenDis = len(distanceList)
	# 根据这个点和往后l个点两点之间的斜率来判断是否是候选解
	epsCandidate = []
	for k in range(lenDis-l):
		if abs(distanceList[k] - distanceList[k+l]) / l <= slope:
			epsCandidate.append(distanceList[k])
	return epsCandidate



def calNeighbors(distanceMatrix, eps, i, data):
	# print(eps)
	neighborPoints = []
	temp = distanceMatrix[i,:]
	# print(type(temp))
	for i in range(len(data)):
		# print(temp[0,i])
		if temp[0,i] < eps and temp[0,i] != 0:
			neighborPoints.append(data[i])

	# print(neighborPoints)
	return neighborPoints


def expandCluster(new_cluster, data, visited, neighborPoints, distanceMatrix, eps, min_pts):

	for point in neighborPoints:
		if point not in visited:
			visited.append(point)
			i = data.index(point)
			subNeighbors = calNeighbors(distanceMatrix,eps,i,data)
			# print(len(subNeighbors))
			if len(subNeighbors) >= min_pts:
				# print("111")
				for pp in subNeighbors:
					if pp not in neighborPoints:
						neighborPoints.append(pp)
						visited.append(pp)

	new_cluster = new_cluster + neighborPoints
	# print(new_cluster)
	return new_cluster, visited








if __name__ == "__main__":
	# 参数初始化
	min_pts = 4 # 最少有6个点
	l = 4
	slope = 0.1
	filepath = 'abc.csv'

	data = readData(filepath)
	distanceMatrix = calDistanceMatrix(data)
	distanceList = getKdistance(min_pts, distanceMatrix)
	x = range(len(distanceList))
	plt.figure()
	plt.plot(x,distanceList)
	#plt.show()
	epsCandidate = calEpsCandidate(distanceList, l, slope)

	while len(epsCandidate) == 0:
		l = input("请输入向前找的点数")
		slope = input("请输入期望的斜率阈值")
		epsCandidate = calEpsCandidate(distanceList, l, slope)

	# 现在参数确定了，min_pts还有eps已知，data已知，可以来DBSCAN聚类了

	eps = epsCandidate[int(len(epsCandidate)/2)]

	config = {'eps':eps,'min_pts':min_pts, 'dim':2}
	dbc = DBScanner(config)
	dbc.dbscan(data)

	










