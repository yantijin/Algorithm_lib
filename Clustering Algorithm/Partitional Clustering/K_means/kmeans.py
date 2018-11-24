#coding=utf-8
from collections import defaultdict
from math import sqrt
from random import uniform


"""
    需要定义的函数：
        计算聚类中心；
        计算两点之间距离；
        将所有点按照距离中心点的距离分类；
        随机生成k个中心点
"""

"""
    计算两点之间的距离
    INPUT: 
        data1,data2: data of the point 
    OUTPUT:
        distance between data1 and data2
"""


def get_distance(data1,data2):
    dimensions = len(data1)
    dis = 0
    for dimension in range(dimensions):
        dis =dis +(data1[dimension]-data2[dimension])**2
    return  sqrt(dis)


"""
    计算聚类中心
    INPUT:
        data_set: an list consists of list
    OUTPUT:
        center: calculate center of the input datas
"""


def cal_center(data_set):
    center = []
    dimensions = len(data_set[0])
    amount = len(data_set)
    for dimension in range(dimensions):
        point_sum = 0
        for data in data_set :
            point_sum = point_sum +data[dimension]
        center.append(point_sum/amount)
    return center


"""
    根据现有分类，重新计算聚类中心
    INPUT:
        assignments: a list that assign each data to a center
        data_set: an list consists of list
    OUTPUT:
        center: update center by the assignments and data_set
"""


def update_center(assignments, data_set):
    center = []
    dt = defaultdict(list)
    for assignment, data in zip(assignments, data_set):
        dt[assignment].append(data)
    for points in dt.values():
        center.append(cal_center(points))
    return center


"""
    将所有点按照距离中心点的距离分类
    INPUT: 
        data_set: an list consists of list
        center: clustering center until now
    OUTPUT:
        assignments: assign each data for a center
"""


def assign_point(data_set, center):
    len_centers = len(center)
    len_data_sets = len(data_set)
    assignments = []
    for len_data_set in range(len_data_sets):
        shortest_dis = float("inf")
        assignment = -1
        for len_center in range(len_centers):
            dis = get_distance(data_set[len_data_set], center[len_center])
            if dis < shortest_dis :
                shortest_dis = dis
                assignment = len_center
        assignments.append(assignment)
    return assignments


"""
    随机生成k个中心点
    INPUT: 
        data_set: an list consists of list
        k: num of centers that wants for clustering
    OUTPUT:
        init_center: init random center 
"""


def generate_init_center(data_set, k):
    dimensions = len(data_set[0])
    center = []
    min_max = defaultdict(float)
    for data in data_set:

        for dimension in range(dimensions):
            min_key = 'min_%d' % dimension
            max_key = 'max_%d' % dimension
            val = data[dimension]
            if min_key not in min_max or val < min_max[min_key]:
                min_max[min_key] = val
            if max_key not in min_max or val > min_max[max_key]:
                min_max[max_key] = val
    # 此步要产生k个在min和max之间的data
    for _k in range(k):
        data = []
        for dimension in range(dimensions):
            min_val = min_max['min_%d' % dimension]
            max_val = min_max['max_%d' % dimension]
            data.append(uniform(min_val, max_val))
        center.append(data)
    return center


"""
    k_means算法实现
    INPUT: 
        data_set: an list consists of list
        k: num of centers that wants for clustering
    OUTPUT:
"""


def kmeans(data_set, k):
    center = generate_init_center(data_set, k)
    assignments = assign_point(data_set, center)
    new_center = update_center(assignments, data_set)
    while new_center != center:
        center = new_center
        assignments = assign_point(data_set, center)
        new_center = update_center(assignments, data_set)
    return zip(assignments, data_set), new_center


"""
    文件读写
"""


def fileread(filepath):
    file_object = open(filepath)
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
            data1=[]

    finally:
        file_object.close()
    return data



if __name__== "__main__":
    filepath = input("请输入文件地址及命名\n")

    data_set = fileread(filepath)
    k = 3
    zip, center = kmeans(data_set, k)
    for i in zip:
        print(i)
    print(center)