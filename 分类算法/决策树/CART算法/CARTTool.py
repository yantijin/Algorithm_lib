from attrNode import *
import sys

class CARTTool:
    YES = "Yes"
    NO = "No"
    attrNum = 0
    data = []
    attrNames = []


    def __init__(self, filePath):
        self.filepath = filePath
        self.attrValue = {}

    """
        读取数据，并将数据存储在data中，属性的数量存在attrNum，属性的名称列表存在attrNames
    """
    def readDataFile(self):
        file_object = open(self.filepath)

        data = []
        data1 = []
        try:
            for line in file_object.readlines():
                tmp = line.replace("\n", "").split(' ')
                tmplen = len(tmp)
                for nm in range(tmplen):
                    data1.append(tmp[nm])
                data.append(data1)
                data1 = []
        finally:
            file_object.close()

        self.data = data
        # print(self.data)
        self.attrNum = len(data[0])
        # print(self.attrNum)
        self.attrNames = data[0]

    """
    初始化属性的值，将每一个属性下的名称存储在attrValue中
    """

    def initAttrValue(self):
        for j in range(self.attrNum):
            tempvalues = []
            for i in range(len(self.data)):
                if i != 0:
                    if self.data[i][j] not in tempvalues:
                        tempvalues.append(self.data[i][j])

                self.attrValue[self.data[0][j]] = tempvalues
        # print(self.attrValue)

    """
        计算Gini系数，此处是二分类，实际上可以多分类
        计算公式为：1-所有可能性平方的和
        remainData:剩余数据
        attrName:想要计算的属性
        value:统计的属性的名称
        belongValue:bool类型，确定是根据属于值来分类还是不属于来分类
    """
    def computeGini(self, remainData, attrName, value, beLongValue):
        posNum = 0
        negNum = 0
        for j in range(1, len(self.attrNames)):
            if attrName == self.attrNames[j]:
                for i in range(1, len(remainData)):
                    # 统计正负实例，按照属于和不属于值的类型进行划分
                    if (beLongValue and remainData[i][j] == value) or (not beLongValue and not remainData[i][j]==value):
                        if remainData[i][len(self.attrNames)-1] == self.YES:
                            posNum += 1
                        else:
                            negNum += 1

        total = posNum + negNum
        # print("posNum:{0},negNum:{1}".format(posNum, negNum))
        if total == 0:
            gini = 1
        else:
            posProbobly = posNum/total
            negProbobly = negNum/total
            gini = 1 - posProbobly*posProbobly - negProbobly*negProbobly

        return gini

    """
    计算所有可能划分属性的基尼系数的增益，并求出最小的，从而知道根据何种属性进行划分
        返回一个str列表，包括miniGini和对应的属性
        remainData:剩余数据
        attrName:属性名称
    """
    def computeAttrGini(self, remainData, attrName):
        str = []
        spiltValue = ""
        miniGini = sys.maxsize
        belongNum = {}
        valueTypes = self.attrValue[attrName]
        for valueType in valueTypes:
            tempNum = 0
            for j in range(len(self.attrNames)):
                if attrName == self.attrNames[j]:
                    for i in range(len(remainData)):
                        if remainData[i][j] == valueType:
                            tempNum +=1
            belongNum[valueType] = tempNum
        # print("belongNum:{0}".format(belongNum))


        posProbably = 1.0
        negProbably = 1.0
        for valueType in valueTypes:
            tempGini = 0
            posProbably = 1.0*belongNum[valueType]/(len(remainData)-1)
            negProbably = 1- posProbably

            tempGini += posProbably * self.computeGini(remainData, attrName, valueType, True)
            tempGini += negProbably * self.computeGini(remainData, attrName, valueType, False)
            # print("posProbably:{0},negProbably:{1},attrName{2},valueType:{3},tempGini:{4}".format(negProbably, posProbably,attrName, valueType, tempGini))

            if tempGini < miniGini:
                miniGini = tempGini
                spiltValue = valueType

        str.append(spiltValue)
        str.append(miniGini)
        return str

    """
    筛选出结点包含的叶子节点的数目
    最终存储在leafNode中
    """

    def addLeafNode(self, node, leafNode):
        if (node.getChildAttrNode() != []):
            for childNode in node.getChildAttrNode():
                dataIndex = childNode.getDataIndex()
                if dataIndex != [] and len(dataIndex) >0:
                    leafNode.append(childNode)
                else:
                    self.addLeafNode(childNode,leafNode)
    """
    计算非叶子结点的误差代价，node为待计算的非叶子结点

    """

    def computeAlpha(self, node):
        rt = 0
        alpha = 0
        sumNum = 0
        minNum = 0
        dataIndex = []
        leafNodes = []
        self.addLeafNode(node, leafNodes)
        # 现在leafNodes中存储的是结点下包含叶子结点的列表
        node.setLeafNum(len(leafNodes))
        # print(node.getLeafNum())
        for attrNode in leafNodes:
            dataIndex = attrNode.getDataIndex()
            num = 0
            sumNum +=len(dataIndex)
            # print(dataIndex)
            for s in dataIndex:

                if self.data[int(s)][len(self.attrNames)-1] == self.YES:
                    num += 1
            minNum += num

            if num/len(dataIndex)>0.5:
                num = len(dataIndex) - num

            rt += (num/(len(self.data)-1))

            if minNum/sumNum >0.5:
                minNum = sumNum - minNum

            Rt = minNum/(len(self.data)-1)
            alpha = (Rt - rt)/(len(leafNodes)-1)
            node.setAlpha(alpha)


    """
    为结点设置序列号，并计算每个节点的误差率，用于后面剪枝
    node:开始的时候传入的是根结点
    index:开始的索引，从1开始
    ifCutNode:是否需要剪枝
    """

    def setIndexAndAlpha(self, node, index, ifCutNode):
        minAlphaNode = None
        minAlpha = sys.maxsize
        nodeQueue = []
        nodeQueue.append(node)
        while len(nodeQueue) > 0:
            index += 1
            tempNode = nodeQueue[0]
            nodeQueue.remove(tempNode)
            tempNode.setNodeIndex(index)
            if tempNode.getChildAttrNode() != []:
                for childNode in tempNode.getChildAttrNode():
                    nodeQueue.append(childNode)
                self.computeAlpha(tempNode)
                if tempNode.getAlpha() < minAlpha:
                    minAlphaNode = tempNode
                    minAlpha = tempNode.getAlpha()
                elif tempNode.getAlpha() == minAlpha:
                    if tempNode.getLeafNum() > minAlphaNode.getLeafNum():
                        minAlphaNode = tempNode

        if ifCutNode:
            minAlphaNode.setChildAttrNode(None)




    """
    属性划分完毕，进行数据的移除
    srcData：源数据
    attrName：划分的属性名称
    valueType:属性的值类型
    """
    def removeData(self, srcData, attrName, valueType, beLongValue):
        defDataArray = []
        desData = []
        # 待删除的数据
        selectData = []
        selectData.append(self.attrNames)
        # 将数组数据转化到列表中，方便移除
        for i in range(len(srcData)):
            desData.append(srcData[i])

        # 从左往右一列列地查找
        for j in range(len(self.attrNames)):
            if self.attrNames[j] == attrName:
                for i in range(len(desData)):
                    if desData[i][j] == valueType:
                        selectData.append(desData[i])

        if beLongValue:
            desDataArray = selectData
        else:
            #属性名称行不移除
            selectData.remove(self.attrNames)
            # 如果是划分不属于此类型的数据时，进行移除
            for tt in selectData:
                desData.remove(tt) # 存在疑问
            desDataArray = desData
        return desDataArray

    # buildDecisionTree(rootnode, "", self.data, remainAttr, False)
    def buildDecisionTree(self, node, parentAttrValue, remainData, remainAttr, belongParentValue):
        valueType = ""
        spiltAttrName = ""
        miniGini = sys.maxsize
        if belongParentValue:
            node.setParentAttrValue(parentAttrValue)
        else:
            node.setParentAttrValue("!"+parentAttrValue)

        if len(remainAttr) == 0:
            if len(remainData) > 1:
                indexArray = []
                for i in range(1,len(remainData)):
                    indexArray.append(remainData[i][0])

                node.setDataIndex(indexArray)
                # print("indexArray:{0}".format(indexArray))
            print("attr remain null")
            return
        for str in remainAttr:
            giniArray = self.computeAttrGini(remainData, str)
            tempGini = float(giniArray[1])
            # print(tempGini, end="")

            if tempGini < miniGini:
                spiltAttrName = str
                miniGini = tempGini
                valueType = giniArray[0]

        remainAttr.remove(spiltAttrName)
        node.setAttrName(spiltAttrName)

        # 分类回归树中，每次二元划分，分出2个孩子节点
        childNode = []
        rData = []
        bArray = [True, False]
        for i in range(len(bArray)):
            rData = self.removeData(remainData, spiltAttrName, valueType, bArray[i])
            # print(rData)
            sameClass = True
            indexArray = []
            for k in range(1,len(rData)):
                indexArray.append(rData[k][0])
                if rData[k][len(self.attrNames)-1] != rData[1][len(self.attrNames)-1]:
                    sameClass = False
                    break
            # print("indexArray:{0}".format(indexArray))
            childNode.append(attrNode())

            if not sameClass:
                rAttr = []
                for str in remainAttr:
                    rAttr.append(str)
                self.buildDecisionTree(childNode[i], valueType, rData, rAttr, bArray[i])
            else:
                if bArray[i]:
                    pAtr = valueType
                else:
                    pAtr = "!"+valueType
                childNode[i].setParentAttrValue(pAtr)
                childNode[i].setDataIndex(indexArray)
                # print("indexArray:{0}".format(indexArray))
        node.setChildAttrNode(childNode)

    def startBuildingTree(self):
        self.readDataFile()
        self.initAttrValue()
        remainAttr = []
        # print(self.attrNames)
        for i in range(len(self.attrNames)-1):
            if i !=0:
                remainAttr.append(self.attrNames[i])
        #print("remainAttr")
        #print(remainAttr)

        rootnode = attrNode()
        self.buildDecisionTree(rootnode, "", self.data, remainAttr, False)
        self.setIndexAndAlpha(rootnode, 0, False)
        print("剪枝前： ",end="")
        self.showDecisionTree(rootnode, 1)
        self.setIndexAndAlpha(rootnode, 0, True)
        print("\n剪枝后：",end="")
        self.showDecisionTree(rootnode,1)


    def showDecisionTree(self,node,blankNum):
        print("\n")
        for i in range(blankNum):
            print("  ", end="")
        print("--", end="")
        # 显示分类的属性值
        if node.getParentAttrValue() != None and len(node.getParentAttrValue()) >0:
            print(node.getParentAttrValue(), end="")
        else:
            print("--", end="")
        print("--", end="")

        if node.getDataIndex() != [] and len(node.getDataIndex())>0:

            i = node.getDataIndex()[0]
            # print(type(self.data[int(i)][len(self.attrNames)-1]))

            print("[{0}]类别:{1}".format(node.getNodeIndex(),self.data[int(i)][len(self.attrNames)-1]),end="")
            print("[",end="")
            for index in node.getDataIndex():
                print(index+",", end="")
            print("]",end="")
        else:

            print("[{0}:{1}]".format(node.getNodeIndex(),node.getAttrName()),end="")
            if node.getChildAttrNode() != None:
                for childNode in node.getChildAttrNode():
                    self.showDecisionTree(childNode,2*blankNum)
            else:
                print("[Child Null]",end="")


if __name__ == "__main__" :
    filePath = "input.txt"
    cart = CARTTool(filePath)
    cart.startBuildingTree()
















