import numpy as np
from numpy import matlib
import matplotlib.pyplot as plt


# 读取数据
# return data type:list
def readData(filepath):
	file_object = open(filepath)
	data = []
	data1 = []
	try:
		for line in file_object.readlines():
			line.replace('\n', '', 1)
			tmp = line.split(',')
			tmplen = len(tmp)
			for nm in range(tmplen):
			   data1.append(float(tmp[nm]))
			data.append(data1[1:])
			data1=[]

	finally:
		file_object.close()
	return data



# 根据参数生成高斯分布
def calGaussian(x, mu, sigma):
	# 首先要知道样本空间的维数
	dim = len(x)
	temp1 = np.exp(-0.5 * np.mat((x - mu)) * np.mat(sigma).I * np.mat((x - mu)).T)
	# print(temp1)
	temp2 = (2 * np.pi)**(dim/2) * np.linalg.det(sigma) ** 0.5
	# print(temp2)
	result = 1 / temp2 * temp1
	# print(result)
	return result



# 计算各个成分生成的后验概率,sigmaVec是一个三个维度的矩阵
def calPosteriorProbability(data, Alpha, muVec, sigmaVec):
	Gamma = np.zeros((len(data), len(muVec)))
	for j in range(len(data)):
		# 计算分母部分
		denominator = 0
		for t in range(len(muVec)):
			# print(data[j])
			# print(muVec[t])
			# print(sigmaVec[t])
			denominator += Alpha[0,t] *  calGaussian(data[j], muVec[t], sigmaVec[t])
		for k in range(len(muVec)):
			# 计算分子部分
			Numrator = Alpha[0,k] * calGaussian(data[j], muVec[k], sigmaVec[k])
			Gamma[j, k] = Numrator / denominator
	# print("gamma:{0}".format(Gamma))
	return Gamma


# M步
def updateParameters(Gamma, data, muVec, sigmaVec, Alpha):
	for i in range(Alpha.shape[1]):
		muVec[i] = Gamma[:,i] * np.mat(data) / np.sum(Gamma[:,i])
		temp =  (np.mat(data) - np.mat(matlib.repmat(muVec[i],len(data),1)))
		# print(temp)
		# print(len(Gamma[:,i]))
		tt = 0
		for k in range(temp.shape[0]):
			tt += Gamma[k,i] * temp[k,:].T * temp[k,:]
		# print(tt.shape)
		sigmaVec[i] = tt / np.sum(Gamma[:,i])
		Alpha[0,i] = np.sum(Gamma[:, i]) / len(data)
		

	return Alpha, muVec, sigmaVec






if __name__ == "__main__":
	# 初始化各个参数
	k = 3; # 高斯混合成分的个数
	data = readData('dataSet.txt')
	m = len(data)
	dim = len(data[0])
	Alpha = 1 / k * np.ones((1,k))
	muVec = np.zeros((k, dim))
	muVec[0] = data[5]
	muVec[1] = data[21]
	muVec[2] = data[26]
	# print(muVec)
	sigmaVec = np.zeros((k,dim,dim))
	for i in range(k):
		sigmaVec[i] = 0.1 * np.eye(dim)


	iter_count = 1
	iterTotal = 100
	while iter_count <= iterTotal:
		Gamma = calPosteriorProbability(data, Alpha, muVec, sigmaVec)
		Alpha, muVec, sigmaVec = updateParameters(Gamma, data, muVec, sigmaVec, Alpha)
		# print("alpha:{0}".format(Alpha))
		# print("sigmaVec:{0}".format(sigmaVec))
		iter_count += 1
	# 下面对点进行划分
	C = {}
	for i in range(k):
		C[i] = []
	for i in range(len(data)):
		maxIndex = np.argmax(Gamma[i,:])
		C[maxIndex].append(data[i])
	
	# print(muVec)
	string = ['b+','y+','r+']
	lenStr = len(string)
	for i in range(k):
		
		plt.plot(muVec[i][0],muVec[i][1],'D')
		for j in range(len(C[i])):
			plt.plot(C[i][j][0], C[i][j][1], string[i % lenStr])
	plt.show()

