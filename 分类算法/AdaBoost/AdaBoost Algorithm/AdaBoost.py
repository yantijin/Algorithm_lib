# coding=utf-8
from point_class import *
from math import log
from math import exp


class AdaBoostTool:
    # 分类类别，程序默认为1和-1
    CLASS_POSITIVE = 1
    CLASS_NEGATIVE = -1

    # 事先假设的三个分类器
    CLASSIFICATION1 = "X=2.5"
    CLASSIFICATION2 = "X=7.5"
    CLASSIFICATION3 = "Y=5.5"
    CLASSIFICATION = [CLASSIFICATION1, CLASSIFICATION2, CLASSIFICATION3]
    CLASSIFICATION_WEIGHT = []
    totalPoint = []

    def __init__(self, filePath, errorValue):
        self._filePath = filePath
        self._errorValue = errorValue

    def readDataFile(self):
        file_object = open(self._filePath)

        data = []
        data1 = []
        try:
            for line in file_object.readlines():
                line.replace('\n', '', 1)
                tmp = line.split(' ')
                tmplen = len(tmp)
                for nm in range(tmplen):
                    data1.append(float(tmp[nm]))
                data.append(data1)
                data1 = []
            print(data)

        finally:
            file_object.close()

        # 下面是将读取的数据存储到totalPoint中
        for array in data:
            tmp = point(array[0], array[1], array[2])
            tmp.setProbably(1.0 / len(data))
            self.totalPoint.append(tmp)


    def calculateWeight(self, errorValue):
        temp = (1 - errorValue) / errorValue

        alpha = 0.5 * log(temp)
        return alpha


    def calculateErrorValue(self, pointMap):
        resultValue = 0
        for key in pointMap:
            tempClassType = int(key)
            pList = pointMap[key]  # 得到类型对应的很多point
            for p in pList:
                temp = p.getProbably()
                print("probably:%f,tempclassType: %f" % (temp, tempClassType))
                if tempClassType != p.getClassType():
                    resultValue += temp

        print("resultValue:")
        print(resultValue)

        weight = self.calculateWeight(resultValue)

        for key in pointMap:
            tempClassType = int(key)
            pList = pointMap[key]
            for p in pList:
                temp = p.getProbably()
                if tempClassType != p.getClassType():
                    temp *= exp(weight)
                    p.setProbably(temp)
                else:
                    temp *= exp(-weight)
                    p.setProbably(temp)

        self.dataNormalized()
        return resultValue


    def dataNormalized(self):
        sumProbably = 0

        for p in self.totalPoint:
            sumProbably += p.getProbably()

        # 归一化处理

        for p in self.totalPoint:
            temp = p.getProbably()
            p.setProbably(temp / sumProbably)


    def classifyData(self, classification, p):
        posPrabably = 0
        negProbably = 0
        isLarger = False  # 判断是否是大于一边的划分
        pList = []

        array = classification.split("=")
        position = array[0]
        value = float(array[1])

        if position == "X":
            if p.getX() > value:
                isLarger = True

            # 将训练数据中所有属于这一边的划分到一起
            for point in self.totalPoint:
                if isLarger and point.getX() > value:
                    pList.append(point)
                elif not isLarger and point.getX() < value:
                    pList.append(point)
        elif position == "Y":
            if p.getY() > value:
                isLarger = True

            for point in self.totalPoint:
                if isLarger and point.getY() > value:
                    pList.append(point)
                elif not isLarger and point.getY() < value:
                    pList.append(point)

        for point in pList:
            if point.getClassType() == self.CLASS_POSITIVE:
                posPrabably += 1
            else:
                negProbably += 1

        if negProbably > posPrabably:
            return self.CLASS_NEGATIVE
        else:
            return self.CLASS_POSITIVE


    def calculateWeightArray(self):
        # CLASSIFICATION_WEIGHT = []

        for i in range(len(self.CLASSIFICATION)):
            mapList = {}
            posPointList = []
            negPointList = []
            for p in self.totalPoint:
                tempClassType = self.classifyData(self.CLASSIFICATION[i], p)

                if tempClassType == self.CLASS_POSITIVE:
                    posPointList.append(p)
                else:
                    negPointList.append(p)

            mapList[self.CLASS_POSITIVE] = posPointList
            mapList[self.CLASS_NEGATIVE] = negPointList

            if i == 0:
                errorValue = self.calculateErrorValue(mapList)
            else:
                errorValue = self.calculateErrorValue(mapList)

            self.CLASSIFICATION_WEIGHT.append(self.calculateWeight(errorValue))


    def adaBoostClassify(self):
        value = 0

        self.calculateWeightArray()

        for i in range(len(self.CLASSIFICATION)):
            print("分类器%d权重为%f" % (i + 1, self.CLASSIFICATION_WEIGHT[i]))
        for j in range(len(self.totalPoint)):
            p = self.totalPoint[j]
            value = 0
            for i in range(len(self.CLASSIFICATION)):
                value += 1.0 * self.classifyData(self.CLASSIFICATION[i], p) * self.CLASSIFICATION_WEIGHT[i]

            # 符号判断

            if value > 0:
                print("点(%d, %d)的组合分类结果为：1，该点的实际分类为%d" % (p.getX(), p.getY(), p.getClassType()))

            else:
                print("点(%d, %d)的组合分类结果为：-1，该点的实际分类为%d" % (p.getX(), p.getY(), p.getClassType()))


if __name__ =="__main__":
    filepath ="input.txt"
    errorValue = 2
    p = AdaBoostTool(filepath, errorValue)
    p.readDataFile()
    # print(p.totalPoint)
    p.adaBoostClassify()











