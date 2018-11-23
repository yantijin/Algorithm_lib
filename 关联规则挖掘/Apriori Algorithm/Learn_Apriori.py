#coding = utf-8
import numpy
from python_util import fileread

"""
    程序所需部分：
        创建初始的候选集
        根据Lk产生Lk+1
        计算每个候选集的支持度
        计算置信度
        generateCandidate（Lk):筛选掉不合适的
        数据读取
"""


"""
    创建初始的候选集
    INPUT：
        data_set:a list of list 存储交易的数据
    OUTPUT:
        C1:列表，每个元素为一个集合
"""


def createInitCandidates(data_set):
    C1 = []
    for data in data_set:
        for item in data:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return [frozenset(c) for c in C1]


"""
    计算支持度
    INPUT:
        data_set:交易数据
        candidate：候选项集合
    OUTPUT:

"""


def calSupport(data_set, candidates):
    # 首先将data_set转化为集合
    support = {}

    datas = [frozenset(data) for data in data_set]
    for candidate in candidates:
        tmp = 0
        for data in datas:
            if candidate.issubset(data):
                tmp += 1
        support[candidate] = tmp/len(data_set)
    return support


"""
    根据支持度来进行筛选掉小于最小支持度的
    INPUT:
        candidates:候选项集合
        min_support:最小支持度
        support：candidates对应的支持度
    OUTPUT:
        new_candidates:即为Lk
"""


def filterCandidates(candidates, min_support, support):
    new_candidates = []
    for candidate in candidates:
        if support[candidate] >= min_support:
            new_candidates.append(candidate)
    new_candidates.sort()
    return new_candidates


"""
    GnenerateCandidates
    INPUT:
        Lk:a list consists of set
    OUTPUT:
        candidates:Ck+1
"""


def generateCandidates(Lk):
    candidates = []
    #找出当前候选项集的长度
    k = len(Lk[0])
    len_Lk = len(Lk)
    #self_joining
    for len_kl1 in range(len_Lk):
        tmp1 = list(Lk[len_kl1])[: k - 1]
        for len_kl2 in range(len_kl1+1, len_Lk):
            tmp2 = list(Lk[len_kl2])[: k - 1]
            if tmp1 == tmp2:
                candidate = Lk[len_kl1].union(Lk[len_kl2])
                candidates.append(candidate)
    candidates.sort()
    return candidates


"""
    Apriori算法实现
    INPUT：
        data_set:数据集，a list consists of list
        min_support:最小支持度
"""


def Apriori(data_set, min_support):
    # 产生初始项集合
    C1 = createInitCandidates(data_set)
    support = calSupport(data_set, C1)
    # 筛选掉小于最小支持度的
    L1 = filterCandidates(C1, min_support, support)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        candidates = generateCandidates(L[k-2])
        tmp_support = calSupport(data_set, candidates)
        Lk = filterCandidates(candidates, min_support, tmp_support)
        #support.append(tmp_support)
        support.update(tmp_support)
        L.append(Lk)
        k += 1
    return support, L




"""
    还需要做的工作：
    输出频繁项集中高于最低值的置信度 两个支持度相除
"""

def calConfidence(supportdata,set1,set2):
    tmp1=[]
    tmp2=[]
    set2.update(set1)
    for key in supportdata:
        if (set1 == key):
            tmp1 = supportdata[key]
        if (set2 == key):
            tmp2 = supportdata[key]
    if tmp1 == [] or tmp2 == []:
        print("小于最小支持度或不存在")
        return 0
    else:
        confidence = tmp2/tmp1
        return confidence



if __name__ == "__main__":
    #pathname = input("请输入文件地址")
    data_set = fileread("testInput.txt")
    support, L = Apriori(data_set, 0.2)
    print("所有项集的支持度为", support)
    print("频繁项集为", L)
    #print(len(support))
    confidence = calConfidence(support, {1}, {2})
    print(confidence)
