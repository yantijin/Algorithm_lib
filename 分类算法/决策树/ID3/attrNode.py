
class attrNode:
    # 当前属性的名字
    # attrName = ""
    # 父亲节点的分类属性值
    parentAttrValue = ""
    # 属性子节点,是一个列表
    childAttrNode = []
    # 孩子叶子结点
    childDataIndex = []
    def __init__(self):
        # 当前属性的名字
        self.attrName = ""

    def getAttrName(self):
        return self.attrName

    def setAttrName(self, attrName):
        self.attrName = attrName

    def getChildAttrNode(self):
        return self.childAttrNode

    def setChildAttrNode(self, childAttrNode):
        self.childAttrNode = childAttrNode

    def getParentAttrValue(self):
        return self.parentAttrValue

    def setParentAttrValue(self, parentAttrValue):
        self.parentAttrValue = parentAttrValue

    def getChildDataIndex(self):
        return self.childDataIndex

    def setChildDataIndex(self, dataIndex):
        self.childDataIndex  = dataIndex
