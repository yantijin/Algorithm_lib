from FPNode import *
from collections import namedtuple
"""
    create an FP_tree
"""


class FPTree(object):
    Route = namedtuple('Route', 'head tail')

    def __init__(self):
        self._root = FPNode(self, None, None)
        self._routes = {}

    def root(self):
        return self._root

    def add(self, transaction):
        # add a transaction to the tree
        point = self._root

        for item in transaction:
            next_point = point.search(item)
            if next_point:
                # 说明现在这个结点的孩子结点里面已经有这个结点了
                next_point.increment()

            else:
                next_point = FPNode(self, item)
                point.add(next_point)
                # next_point.parent(point)
                # update the route that contains this item to include our new node

                self._update_route(next_point)
            point = next_point
            print(self._routes)

    def _update_route(self, point):
        # 根据此节点的item加进对应的route中
        assert self is point.tree()
        try:
            route = self._routes[point.item()]
            route[1]._neighbor = point  # route[1]是包含item项的整个路径的尾部
            self._routes[point.item()] = self.Route(route[0], point)
        except KeyError:
            # 说明是包含此item的第一个节点，需要创建并加入
            self._routes[point.item()] = self.Route(point, point)
        #print(self._routes)

    def nodes(self, item):
        # 产生一个包含给定item的节点构成的序列
        try:
            node = self._routes[item][0] # 尾部
        except KeyError:
            return
        while node and not node.root():
            yield node
            node = node._neighbor

    def items(self):
        # 产生一个包含两个元组的表现形式，(item, nodes(item))
        for item in self._routes.keys():
            yield (item, self.nodes(item))

    def prefix_paths(self, item):
        # 产生一个最后一个元素包含item的路径
        def collect_path(node):
            path = []
            # print("line175")
            # print(node.root())
            # print(node.root)
            # print(type(node.root()))
            while node and not node.root():
                path.append(node)
                node = node.parent()
            path.reverse()
            return path
        # for node in self.nodes(item):
            # print(node)
            # print("line182")
            # print(collect_path(node))
        return (collect_path(node) for node in self.nodes(item))

    def inspect(self):
        print('Tree:')
        self._root.inspect(1)

        print("\n")
        print('Routes')
        for item, nodes in self.items():
            print(' %r' % item)
            for node in nodes:
                print('      %r' % node)
