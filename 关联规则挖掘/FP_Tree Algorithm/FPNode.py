
"""
    创建FPNode
"""


class FPNode(object):

    def __init__(self, tree, item, count=1):
        # 初始化过程
        self._tree = tree
        self._item = item
        self._count = count
        self._parent = None
        self._children = {}
        self._neighbor = None

    # 下面几个函数为获取叶子节点中的参数

    def tree(self):
        return self._tree

    def count(self):
        return self._count

    def item(self):
        return self._item

    def parent(self):
        return self._parent

    def neighbor(self):
        return self._neighbor

    def children(self):
        return tuple(self._children.values())
    # --------------------------------

    def add(self, child):
        # child is an FP_node, add as a child of this children
        if not isinstance(child, FPNode):
            raise TypeError("We can only add an FPNode as a child")
        # print("line56")
        # print(type(child.item()))
        if child.item() not in self._children:
            self._children[child.item()] = child
            child._parent = self

    def search(self, item):
        # find whether this node contains a child node for the given items
        try:
            return self._children[item]
        except KeyError:
            return None

    def __contains__(self, item):
        # 判断是否item包含在节点的孩子结点中
        return item in self._children

    def increment(self):
        # 对FPNode的count+1
        if self._count is None:
            raise ValueError("Root nodes have no amount")
        self._count += 1

    def root(self):
        # 判断是否为根结点
        return self._item is None and self._count is None

    def leaf(self):
        # 判断是否是叶子节点
        return len(self._children) == 0

    def setParent(self, value):
        # 设置该节点的parent节点
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as parent")
        if value and value.tree is not self.tree:
            raise ValueError("cannot have a parent from another tree")
        self._parent = value

    def setNeighbor(self, value):
        if value is not None and not isinstance(value, FPNode):
            raise TypeError("A node must have an FPNode as neighbor")
        if value and value.tree is not self.tree:
            raise ValueError("cannot have a neighbor from another tree")
        self._neighbor = value

    def __repr__(self):
        if self.root():
            return "<%s (root)>" % type(self).__name__
        return "<%s %r (%r)>" % (type(self).__name__, self.item(), self.count())

    def inspect(self, depth=0):
        print((' ' * depth) + repr(self))
        for child in self._children:
            child.inspect(depth + 1)
