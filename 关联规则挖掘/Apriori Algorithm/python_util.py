



def fileread(filepath):
    """
        文件读取
    """
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