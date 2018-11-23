from attrNode import *
from DataNode import *
from math import log2

class ID3Tool:
    YES = "Yes"
    NO = "No"
    # 所有属性的类型总数
    attrNum = 0
    data = []
    attrNames = []

    def __init__(self, filePath):
        self.filePath = filePath
        self.attrValue = {}

    """
    读取数据,
    将源数据存储于data中
    属性的长度存储于attrNum中
    各个属性的名字存储于attrNames中
    """

    def readDataFile(self):
        file_obj = open(self.filePath)

        data = []
        data1 = []
        try:
            for line in file_obj.readlines():
                tmp = line.replace("\n","").split(' ')
                tmplen = len(tmp)
                for nm in range(tmplen):
                    data1.append(tmp[nm])
                data.append(data1)
                data1 = []
        finally:
            file_obj.close()
        self.data = data
        self.attrNum = len(data[0])
        self.attrNames = data[0]

    """
    初始化属性的值
    将每个属性下面的值存储到一个map对象attrValue中去
    """
    def initAttrValue(self):
        for j in range(1,self.attrNum):
            tempValues = []
            for i in range(1,len(self.data)):
                if self.data[i][j] not in tempValues:
                    tempValues.append(self.data[i][j])
            self.attrValue[self.data[0][j]] = tempValues

    """
    计算熵的值
    remainData:剩余数据
    attrName:待划分的属性
    value:划分的子属性
    isParent:是否分子属性划分还是原来不变的划分
    """

    def computeEntropy(self, remainData, attrName, value, isParent):
        total = 0
        posNum = 0
        negNum = 0
        for j in range(1, len(self.attrNames)):
            if attrName == self.attrNames[j]:
                for i in range(1, len(remainData)):
                    if isParent or (not isParent and remainData[i][j] == value):
                        if remainData[i][len(self.attrNames)-1] == self.YES:
                            posNum += 1
                        else:
                            negNum += 1
        total = posNum + negNum
        if total == 0:
            return 0
        else:
            posProbably = posNum/total
            negProbably = negNum/total

            if posProbably == 1 or posProbably == 0:
                return 0
            entropyValue = -posProbably*log2(posProbably)- negProbably*log2(negProbably)
        return entropyValue


    """
    为某个属性计算信息增益
    remainData 剩余数据
    value 待划分的属性
    """
    def computeGain(self,remainData, value):
        # 属性的种类数
        attrTypes = list(self.attrValue[value])
        print("attrTypes:{0}".format(attrTypes))
        # 增益
        gainValue = 0
        # 原来熵的大小会和划分之后作比较
        entropyOri = 0
        # 子划分熵的和
        childEntropySum = 0
        # 属性子类型的个数
        childValueNum = 0
        # 子属性对应的权重比
        ratioValues = {}

        # 首先统一计数为0
        for i in attrTypes:
            ratioValues[i] = 0

        for j in range(1,len(self.attrNames)):
            if value == self.attrNames[j]:
                for i in range(1,len(remainData)-1):
                    childValueNum = ratioValues[remainData[i][j]]
                    childValueNum += 1
                    ratioValues[remainData[i][j]] = childValueNum

        # 计算原来熵的大小
        entropyOri  = self.computeEntropy(remainData, value, None, True)

        for i in range(len(attrTypes)):
            ratio = float(ratioValues[attrTypes[i]])/(len(remainData)-1)
            childEntropySum += ratio * self.computeEntropy(remainData, value, attrTypes[i], False)


        gainValue = entropyOri - childEntropySum
        return gainValue

    """
    计算信息增益比
    remainData:剩余数据
    value:待划分的属性
    """
    def computeGainRatio(self,remainData, value):
        gain = 0
        spiltInfo = 0
        childValueNum = 0
        attrTypes = list(self.attrValue[value])

        ratioValues = {}

        # 首先统一计数为0
        for i in attrTypes:
            ratioValues[attrTypes[i]] = 0

        for j in range(1, len(self.attrNames)):
            if value == self.attrNames[j]:
                for i in range(1, len(remainData)-1):
                    childValueNum = ratioValues[remainData[i][j]]
                    childValueNum += 1
                    ratioValues[remainData[i][j]] = childValueNum

        gain = self.computeGini(remainData, value)

        for i in len(attrTypes):
            ratio = float(ratioValues[attrTypes[i]])/(len(remainData)-1)
            spiltInfo += -ratio * log2(ratio)

        return gain/spiltInfo

    """
    利用源数据构造决策树
    """
    def buildDecisionTree(self,node, parentAttrValue,remainData, remainAttr, isID3):
        attrName = ""
        gainValue = 0
        tempValue = 0

        if len(remainData) == 1:
            print("attr Null")
            return

        # 选择剩余属性中信息增益最大的作为下一个分类的属性
        for i in range(len(remainAttr)):
            # 判断是用ID3算法还是C4.5算法
            if isID3:
                # ID3采用的是按照信息增益的值来进行比较
                tempValue = self.computeGain(remainData, remainAttr[i])
            else:
                tempValue = self.computeGainRatio(remainData, remainAttr[i])

            if tempValue > gainValue:
                gainValue = tempValue
                attrName = remainAttr[i]

        node.setAttrName(attrName)
        valueTypes = self.attrValue[attrName]
        remainAttr.remove(attrName)

        rData = []
        childNode = []
        for i in range(len(valueTypes)):
            rData = self.removeData(remainData, attrName, valueTypes[i])
            childNode.append(attrNode())
            sameClass = True
            indexArray = []
            for k in range(1, len(rData)):
                indexArray.append(rData[k][0])
                # 判断是否是同一类的
                if rData[k][len(self.attrNames)-1] != rData[1][len(self.attrNames)-1]:
                    sameClass = False
                    break

            if not sameClass:
                rAttr = []
                for str in remainAttr:
                    rAttr.append(str)

                self.buildDecisionTree(childNode[i], valueTypes[i],rData,rAttr, isID3)
            else:
                childNode[i].setParentAttrValue(valueTypes[i])
                childNode[i].setChildDataIndex(indexArray)
        node.setChildAttrNode(childNode)

    """
    属性划分完毕,进行数据的移除
    srcData 源数据
    attrName:划分的属性名称
    valueType:属性的值的类型
    """
    def removeData(self, srcData, attrName, valueType):
        desDataArray = []
        desData = []
        # 待删除的数据
        selectData = []
        selectData.append(self.attrNames)
        for i in range(len(srcData)):
            desData.append(srcData[i])

        for j in range(1, len(self.attrNames)):
            if self.attrNames[j] == attrName:
                for i in range(1, len(desData)):
                    if desData[i][j] == valueType:
                        selectData.append(desData[i])

        desDataArray = selectData
        return desDataArray

    """
    开始构建决策树
    IsID3:是否采用ID3算法构建决策树
    """
    def startBuildingTree(self,isID3):
        self.readDataFile()
        self.initAttrValue()

        remainAttr = []
        for i in range(1,len(self.attrNames)-1):
            remainAttr.append(self.attrNames[i])
        rootNode = attrNode()
        self.buildDecisionTree(rootNode,"",self.data,remainAttr,isId3)
        self.showDecisionTree(rootNode, 1)

    """
    显示决策树
    node: 待显示的结点
    blankNum:行空格符,用于显示树型结构
    """
    def showDecisionTree(self, node, blankNum):
        print("")
        for i in range(blankNum):
            print("\t",end="")
        print("--",end="")

        # 显示分类的属性值
        if node.getParentAttrValue() != None and len(node.getParentAttrValue())>0:
            print(node.getParentAttrValue(),end="")
        else:
            print("--",end="")

        print("--",end="")

        if node.getChildDataIndex() != None and len(node.getChildDataIndex())>0:
            i = node.getChildDataIndex()[0]
            print("类别:{0}".format(self.data[int(i)][len(self.attrNames)-1]),end="")
            print("[",end="")
            for index in node.getChildDataIndex():
                print(index+",",end="")

            print("]",end="")
        else:
            print("[{0}]".format(node.getAttrName()))
            for childNode in node.getChildAttrNode():
                self.showDecisionTree(childNode,2*blankNum)
if __name__ =="__main__":
    filepath = "input.txt"
    p = ID3Tool(filepath)
    p.readDataFile()
    isId3 = True
    p.startBuildingTree(isId3)
    # p.showDecisionTree()








