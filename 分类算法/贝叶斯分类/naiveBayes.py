def createDataSet():
	"""
	创建测试的数据集
	:return:
	"""
	dataSet = [
		# 1
		['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
		# 2
		['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
		# 3
		['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
		# 4
		['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', '好瓜'],
		# 5
		['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', '好瓜'],
		# 6
		['青绿', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '好瓜'],
		# 7
		['乌黑', '稍蜷', '浊响', '稍糊', '稍凹', '软粘', '好瓜'],
		# 8
		['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '硬滑', '好瓜'],

		# ----------------------------------------------------
		# 9
		['乌黑', '稍蜷', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜'],
		# 10
		['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', '坏瓜'],
		# 11
		['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', '坏瓜'],
		# 12
		['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', '坏瓜'],
		# 13
		['青绿', '稍蜷', '浊响', '稍糊', '凹陷', '硬滑', '坏瓜'],
		# 14
		['浅白', '稍蜷', '沉闷', '稍糊', '凹陷', '硬滑', '坏瓜'],
		# 15
		['乌黑', '稍蜷', '浊响', '清晰', '稍凹', '软粘', '坏瓜'],
		# 16
		['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', '坏瓜'],
		# 17
		['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', '坏瓜']
	]

	# 特征值列表
	labels = ['色泽', '根蒂', '敲击', '纹理', '脐部', '触感']

	# 特征对应的所有可能的情况
	labels_full = {}

	for i in range(len(labels)):
		labelList = [example[i] for example in dataSet]
		uniqueLabel = set(labelList)
		labels_full[labels[i]] = uniqueLabel

	return dataSet, labels, labels_full

def calAttribute(dataSet, labels, labels_full):
	# 统计每个属性好坏瓜的数量
	resultTotal = {}
	resultGood = {}
	for label in labels:
		resultGood[label] = {}
		resultTotal[label] = {}
	for label in labels:
		for attr in labels_full[label]:
			if attr not in resultTotal:
				resultTotal[label][attr] = 0
			if attr not in resultGood:
				resultGood[label][attr] = 0
			for i in range(len(dataSet)):
				if attr in dataSet[i]:
					if dataSet[i][-1] == '好瓜':
						resultGood[label][attr] += 1
					resultTotal[label][attr] += 1


	return resultTotal, resultGood

def calTotalNum(dataSet):
	totalNum = len(dataSet)
	return totalNum

def calGoodNum(dataSet):
	labelGood = 0
	for i in range(len(dataSet)):
		if dataSet[i][-1] == '好瓜':
			labelGood += 1
	return labelGood

def calClassPriorProbability(totalNum, labelGood):
	# 计算类先验概率,使用Laplace修正，防止有未出现的属性让概率乘起来为0
	P_good = (labelGood + 1) / (totalNum + 2)
	P_bad = (totalNum - labelGood + 1) / (totalNum +2)
	return P_good, P_bad

def calAttrConditionalProbability(labels, resultTotal, resultGood):
	# 计算属性的条件概率
	P_yes = {}
	P_no = {}
	for label in labels:
		P_yes[label] = {}
		P_no[label] = {}
	for label in labels:
		for attr in resultGood[label]:
			P_yes[label][attr] = (resultGood[label][attr] + 1) / (resultTotal[label][attr] + len(resultGood[label]))
			P_no[label][attr] = (resultTotal[label][attr] - resultGood[label][attr] + 1) / (resultTotal[label][attr] + len(resultGood[label]))

	return P_yes, P_no

def naiveBayesDecision(data):
	# 仅做测试用，实际可以输入
	if data == None:
		data = ['青绿','蜷缩','浊响','清晰','凹陷','硬滑']
	dataSet, labels, labels_full = createDataSet()
	totalNum = calTotalNum(dataSet)
	labelGood = calGoodNum(dataSet)
	P_good, P_bad = calClassPriorProbability(totalNum, labelGood)
	resultTotal, resultGood = calAttribute(dataSet, labels, labels_full)
	P_yes, P_no = calAttrConditionalProbability(labels, resultTotal, resultGood)
	Pro_yes = P_good
	Pro_no = P_bad
	for i in range(len(data)):
		Pro_yes *= P_yes[labels[i]][data[i]]
		Pro_no *= P_no[labels[i]][data[i]]
	if Pro_yes >= Pro_no:
		print("Good, enjoy it!")
	else:
		print("emm，this is a bad watermelon")

if __name__ == '__main__':
	naiveBayesDecision(None)
