import numpy as np 
import matplotlib.pylab as plt
import matplotlib
import operator
import collections

# 收集数据
# 准备数据
# 分析数据
# 训练数据
# 测试算法
# 使用算法


def file2matrix(filename):
    """
    Desc: 
        导入数据
    Para:
        filename: 数据文件路径
    return:
        数据矩阵 returnMat
        对应的类别 classLabelVector    
    """
    numberOfLines = len(open(filename).readlines())
    fr = open(filename) # 重新打开文件流
    returnMat = np.zeros(shape=(numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in fr.readlines():
        line = line.strip() # 去掉首位的空白
        lineFormLine = line.split('\t') # 按照制表符'\t'划分行
        returnMat[index, :] = lineFormLine[0:3]
        classLabelVector.append(int(lineFormLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    """
    Desc: 归一化特征值,消除特征之间数量及不同导致的影响
    para:
        dataSet: 数据集
    return:
        归一化后的数据集
    归一化公式:
        Y = (X - Xmin) / (Xmax - Xmin)
    """
    minValues = dataSet.min(axis=0) # 列最小值
    maxValues = dataSet.max(axis=0)
    ranges = maxValues - minValues # 极差
    normDataSet = (dataSet - minValues) / ranges
    # 不采用手工填充直接计算的方法
    # ====================start=========================
    # m = dataSet.shape[0] # 行数
    # dataSet -= np.tile(minValues, (m,1)) # 填充m行
    # dataSet /= np.tile(ranges, (m,1))
    # normDataSet = dataSet
    # ====================end===========================
    return normDataSet 


def classify(inX, dataSet, labels, k): # K临近
    """
    Desc: 计算输入向量与数据集的距离
    para:
        inX:  输入向量 inX=[1,2,3]
        dataSet: 全体数据集 dataSet=[[1,2,3],[2,3,4]]
        labels:  标签向量
        k: 选择最近邻居的数量
    return:
        预测的类别
    """
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    distance = sqDiffMat.sum(axis=1) # 行相加
    sqDistance = distance ** 0.5
    sortedDistanceIndices = sqDistance.argsort() # 升序返回索引

    classCount = {}
    for i in range(k):
        voteLabel = labels[sortedDistanceIndices[i]]
        classCount[voteLabel] = classCount.get(voteLabel, 0) + 1 
        # 字典的get(k,d)相当于if...else... 如果有返回键k对应的值否则返回d
    sortedClassCount = sorted(classCount, key=operator.itemgetter(1), reverse=True)
    # 排序字典, key=operator.itemgetter(1,0) 实现多级排序, 先排序字典的值,再排序字典的键
    
    # 等效于
    # ====================start================================
    # dist = np.sum((dataSet-inX)**2,axis=1)**0.5
    # k_labels = [labels[index] for index in dist.argsort()[0:k]]
    # label = collections.Counter(k_labels).most_common(1)[0][0] # most_common(1) 返回元祖(a,b) ,故取[0][0]返回出现最多的元素本身
    # return label
    # collections.Counter(k).most_common(1) 返回(a,b) a是出现最多的元素, b是出现最多的元素的次数
    # ====================end==================================

    return sortedClassCount[0][0] # 返回最邻近的标签


def classifyPerson(): 
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentVG = float(input('percentage of time spent playing video games ?'))
    ffMiles = float(input('frequent filer miles earned pre year?'))
    iceCream = float(input('liter of ice cream consumed per year?'))


def datingClassTest():
    """
    Desc: 测试方法
    para: 
        none
    return:
        错误数
    """
    testRatio = 0.1
    dataingDataMat, dataingLabels = file2matrix('datingTestSet2.txt')
    normMat = autoNorm(dataingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*testRatio)
    print('numTestVecs=', numTestVecs)
    errCnt = 0
    for i in range(numTestVecs):
        classifierResult = classifierResult = classify(normMat[i,:], normMat[numTestVecs:m,:], dataingLabels[numTestVecs:m], 3)
        if classifierResult != dataingLabels[i]:
            errCnt += 1.0
    print('the total error rate is: %f' % (errCnt / numTestVecs))
    return  errCnt    


if __name__ == '__main__':
    datingMat, datingLabel = file2matrix('datingTestSet2.txt')
    normDataSet1= autoNorm(datingMat)
    a = (1, 2, 1, 3, 1, 1)
    print(collections.Counter(a).most_common(1))


        
