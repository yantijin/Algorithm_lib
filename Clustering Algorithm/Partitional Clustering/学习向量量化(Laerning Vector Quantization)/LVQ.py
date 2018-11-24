from math import sqrt
import numpy as np
import random



def fileReader(filepath):
	file_object = open(filepath)
	data = []
	data1 = []
	dataRange = []
	try:
		for line in file_object.readlines():
			line.replace('\n', '', 1)
			tmp = line.split(' ')
			tmplen = len(tmp)
			for nm in range(tmplen):
			   data1.append(float(tmp[nm]))
			data.append(data1)
			data1=[]
		tt = np.array(data)
		dataRange.append(tt.min(axis = 0))
		dataRange.append(tt.max(axis = 0))
	finally:
		file_object.close()
	return data, dataRange



def calDistance(vec1, vec2):
	a = len(vec1)
	b = len(vec2)
	if a != b:
		print("向量长度不一致，请重新检查")
		return
	distance = 0
	for i in range(a):
		distance += (vec1[i] - vec2[i])**2
	distance = sqrt(distance)
	return distance


def findNearestPoint(vec1, pointList):
	distance = np.inf
	nearestPoint = vec1
	index = -1
	for pointIndex in range(len(pointList)):
		# print("vec1 {0},point,{1}".format(vec1,pointList[pointIndex]))
		temp = calDistance(vec1, pointList[pointIndex])
		if temp < distance:
			distance = temp
			nearestPoint = pointList[pointIndex]
			index = pointIndex
	return nearestPoint, index


# 初始化原型向量，q为原型向量个数，vecLen为每个向量的长度
# range为每一个维数的range
def initPrototypeVector(q, vecLen,dimRange):
	PrototypeVec = []
	tempPrototype = []
	for i in range(q):
		for j in range(vecLen):
			temp = dimRange[0][j] + (dimRange[1][j] - dimRange[0][j]) * np.random.random()
			tempPrototype.append(temp)
		PrototypeVec.append(tempPrototype)
		tempPrototype = []
		# print(PrototypeVec)
	return PrototypeVec

if __name__ == "__main__":
	# 初始化参数
	q = 3
	filepath = 'input.txt'
	data, dataRange = fileReader(filepath)
	vecLen = len(data[0])
	# 学习率
	eta = 0.2
	# print(dataRange)
	PrototypeVec = initPrototypeVector(q, vecLen, dataRange)
	# 生成预判标记
	predictVec = [2,2,0,0,0,1]
	#for i in range(q):
	#	predictVec.append(random.randint(0, q-1))

	# 已知的标记
	y = [0,0,0,1,2,2]
	gen  = 0
	maxGen = 1000
	while gen <= maxGen:
		 l = random.randint(0, len(data)-1)
		 vec = data[l]
		 point, index = findNearestPoint(vec, PrototypeVec)
		 if y[l] == predictVec[index]:
		 	temp = np.array(predictVec[index]) + eta * (np.array(vec) - np.array(predictVec[index]))
		 	PrototypeVec[index] = list(temp)
		 else:
		 	temp = np.array(predictVec[index]) - eta * (np.array(vec) - np.array(predictVec[index]))
		 gen += 1

	print(PrototypeVec)



