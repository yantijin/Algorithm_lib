import numpy as np




def  readData(path):
	KPI_ID = []
	TS = []
	TS_time = []
	data = []
	data_time = []
	with open(path) as file:
		for line in file.readlines():
			tmpdata = line.split(',')
			TS_time.append(int(tmpdata[0]))
			TS.append(float(tmpdata[1]))
			if tmpdata[-1] not in KPI_ID:
				KPI_ID.append(tmpdata[-1])
				data.append(TS)
				data_time.append(TS_time)
				TS_time = []
				TS = []
	return data, data_time

'''
@param alpha: 置信水平，默认为0.05，对应Zalpha = 1.65
@param epsilon: 容忍上限，默认为0.01
@param m: 根据你的聚类算法设定
@param pi: 1%
'''
def calSampleSize(m, epsilon=0.01, alpha=0.05, pi=0.01):
	S = []
	if alpha == 0.05:
		Zalpha = 1.65
		Zalpha2 = 1.96
	S_min = (m + Zalpha*(Zalpha/2 +sqrt(m+Zalpha^2/4))) / pi;
	S_max = (Zalpha2^2) / (4 * epsilon^2)
	S.append[S_min]
	S.append[S_max]
	return S


def PAA(TS, d):
	D = len(TS)
	new_TS = []
	for i in range(d):
		tmp = 0
		for j in range(D/d*i, D/d*(i+1)):
			tmp += TS[j]
		new_TS.append(tmp/D*d)
		tmp = 0
	return new_TS


def calTypicalFrequency(TS):
	g = calAutoCorrelation(TS)
	for i in range(1, len(g)-1):
		if g[i] < g[i-1] and g[i+1] > g[i]:
			return g[i]


def calAutoCorrelation(TS):
	a = np.fft.fft(TS)
	tt = a * np.conj(a)
	g = np.fft.ifft(tt)
	return g








if __name__  == "__main__":
	readData("test.csv")