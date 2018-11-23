from collections import namedtuple
from collections import defaultdict
from FP_Tree import *
from FPNode import *


"""
    实现FP_Growth算法需要用到的函数：
        统计每个项目出现的次数，将低于minSupport的筛选掉，剩下的按照次数降序排列得到F1
        按照降序排列的顺序对数据重新排列，不在F1中的直接删除，得到的集合为当前CPB(Conditional Pattern Base)
        构建FP_Tree，并要求将相同名称的节点连接起来，每个节点有两个属性，name和count，表头项为项目的总次数
        遍历表头项中的每一项，而后new_postList=[old_postList 表头项]，postList表示的是频繁模式，
        找到FP_Tree中的所有的节点，从根结点到项目节点，且设置每个节点的count为项目节点的count
        去掉最后的项目节点，构成新的CPB，而后递归调用FPG(Growth)，直到有一个CPB为空为止。
"""

def conditional_tree_from_paths(paths):
    # 通过给定的路径创建一个条件FP_tree
    tree = FPTree()
    condition_item = None
    items = set()
    # 根据路径中包含的节点来创建新的树，其中，只有叶子节点的count属性是有用的，其他都要赋值为此count
    for path in paths:
        # print("line201")
        # print(path)
        if condition_item is None:
            condition_item = path[-1].item()
        point = tree.root()
        for node in path:
            next_point = point.search(node.item())
            if not next_point:
                # 创建一个新的结点
                items.add(node.item())
                count = node.count() if node.item() == condition_item else 0
                next_point = FPNode(tree, node.item(), count)
                point.add(next_point)
                tree._update_route(next_point)

            point = next_point
    assert condition_item is not None

    # 将非叶子节点的count记为叶子节点的count
    for path in tree.prefix_paths(condition_item):
        count = path[-1].count()
        for node in reversed(path[:-1]):
            print("line216")
            print(type(node))
            node._count += count
    return tree


def find_frequent_itemsets (transactions, minimum_support, include_support=False):
    items = defaultdict(lambda: 0) # mapping from items to their supports

    # 找到每个item的数量
    for transaction in transactions:
        for item in transaction:
            items[item] += 1

    # 删除掉小于最小支持度的项目
    items = dict((item, support) for item, support in items.items() if support >= minimum_support)
    # 构造一个新的FP_tree，删除掉低于minimum_support的，
    # 而后按照出现的频繁度降序排列
    print("line 238,items")
    print(items)
    def clean_transaction(transaction):
        transaction = list(filter(lambda v: v in items, transaction))
        transaction.sort(key=lambda v: items[v], reverse=True)
        return transaction

    master = FPTree()
    print("transaction:")
    for transaction in list(map(clean_transaction, transactions)):
        print(transaction)
        master.add(transaction)

    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            # print(item)
            # cprint(type(nodes))
            # print("----------------")
            # for n in nodes:
                # print(type(n))
                # print("line84")
                # print(n.count())
                # print(n)
            # support = 0
            # for n in nodes:
                # support += n._count
            support = sum(n._count for n in nodes)
            # print("line264")
            # print(item)
            # print(support)
            if support >= minimum_support and item not in suffix:
                found_set = [item] + suffix
                yield (found_set, support) if include_support else found_set

                # 构建一个conditional tree 并且迭代搜索频繁项
                #print("line99")
                #print(tuple(tree.prefix_paths(item)))
                cond_tree = conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s
    for itemset in find_with_suffix(master, []):
        yield itemset

if __name__ == '__main__':

    from optparse import OptionParser
    import csv

    p =OptionParser(usage='%prog data_file')
    p.add_option('-s', '--minimum-support', dest='minsup', type='int',
                 help='Minimum itemset support(default: 2)')
    p.add_option('-n', '--numeric', dest='numeric', action='store_true',
                 help='Convert the values in datasets to numerals (default: false)')
    p.set_defaults(minsup=2)
    p.set_defaults(numeric=False)

    options, args = p.parse_args()
    if len(args) < 1:
        p.error('must provide the path to a CSV file to read')

    transactions = []
    with open(args[0]) as database:
        for row in csv.reader(database):
            if options.numeric:
                transaction = []
                for item in row:
                    transaction.append(item)
                transactions.append(transactions)
            else:
                transactions.append(row)
    result =[]
    for itemset, support in find_frequent_itemsets(transactions, options.minsup, True):
        result.append((itemset, support))

    result = sorted(result, key=lambda i: i[0])
    for itemset, support in result:
        print(str(itemset)+' '+str(support))
