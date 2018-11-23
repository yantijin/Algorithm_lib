class attrNode(object):

    nodeIndex = 0
    leafNum = 0
    alpha = 0
    parentAttrValue = None
    childAttrNode = []
    dataIndex = []
    def __init__(self):
        attrName = ""



    def getAttrName(self):
        return self.attrName

    def setAttrName(self, value):
        self.attrName = value

    def getNodeIndex(self):
        return self.nodeIndex

    def setNodeIndex(self, nodeIndex):
        self.nodeIndex = nodeIndex

    def getAlpha(self):
        return self.alpha

    def setAlpha(self, value):
        self.alpha = value

    def getParentAttrValue(self):
        return self.parentAttrValue

    def setParentAttrValue(self, value):
        self.parentAttrValue = value

    def getChildAttrNode(self):
        return self.childAttrNode

    def setChildAttrNode(self, childNode):
        self.childAttrNode = childNode

    def getDataIndex(self):
        return self.dataIndex

    def setDataIndex(self, dataIndex):
        self.dataIndex = dataIndex

    def getLeafNum(self):
        return self.leafNum

    def setLeafNum(self, leafNum):
        self.leafNum = leafNum




