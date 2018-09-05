# -*- coding: utf-8 -*-
"""
一些共用的的数据处理的函数
该模块所包含的函数至少被两个或两个以上其他模块调用和使用
"""


import numpy as np
import xlwt
import scipy.io as scio
import random
import os


def _ZCR(data):
    """
    计算输入数据流的过0次数
    :param data:要分析的手势数据的数据流
    :return:过0次数
    """
    # 输入是numpy的一维数组
    # 输出是过零率
    zcrSum = 0
    len = np.size(data)
    for i in range(len):
        if i >= 1:
            result = np.abs(np.sign(data[i]) - np.sign(data[i - 1]))
            zcrSum = zcrSum + result
    return zcrSum


def featureGet(emgDataAll, imuDataAll, divisor=8):
    global debug
    # 初始参数
    """
    获取单手手势运动数据的特征
    :param emgDataAll:  emg数据，可以是list也可以是array
    :param imuDataAll: imu数据，可以是list也可以是array
    :param divisor: 分片数
    :return: 返回特征
    """
    debug = debug + 1
    emgDataAll = np.array(emgDataAll)
    imuDataAll = np.array(imuDataAll)
    frq = 50  # 采样频率50Hz
    lenData = len(emgDataAll[:, 1])
    reminder = np.mod(lenData, divisor)
    lenData = lenData - reminder
    windows = int(lenData / divisor)
    feature = []
    for j in range(divisor):
        # 数据预处理，归一化，无量纲化
        # 转成数组
        emgData = emgDataAll[0 + j * windows:windows + j * windows, :]
        imuData = imuDataAll[0 + j * windows:windows + j * windows, :]
        accX = imuData[:, 0]
        accY = imuData[:, 1]
        accZ = imuData[:, 2]
        gcoX = imuData[:, 3]
        gcoY = imuData[:, 4]
        gcoZ = imuData[:, 5]
        emg1 = emgData[:, 0]
        emg2 = emgData[:, 1]
        emg3 = emgData[:, 2]
        emg4 = emgData[:, 3]
        emg5 = emgData[:, 4]
        emg6 = emgData[:, 5]
        emg7 = emgData[:, 6]
        emg8 = emgData[:, 7]
        acc = np.sqrt(accX**2 + accY**2 + accZ**2)
        # 特征提取
        # 差分
        diffAccX = np.diff(accX)
        diffAccY = np.diff(accY)
        diffAccZ = np.diff(accZ)
        gco = np.sqrt(gcoX**2 + gcoY**2 + gcoZ**2)
        diffGcoX = np.diff(gcoX)
        diffGcoY = np.diff(gcoY)
        diffGcoZ = np.diff(gcoZ)
        # 均值
        meanAccX = np.mean(accX)
        meanAccY = np.mean(accY)
        meanAccZ = np.mean(accZ)
        meanGcoX = np.mean(np.abs(gcoX))
        meanGcoY = np.mean(np.abs(gcoY))
        meanGcoZ = np.mean(np.abs(gcoZ))
        meanDiffAccX = np.mean(np.abs(diffAccX))
        meanDiffAccY = np.mean(np.abs(diffAccY))
        meanDiffAccZ = np.mean(np.abs(diffAccZ))
        meanDiffGcoX = np.mean(np.abs(diffGcoX))
        meanDiffGcoY = np.mean(np.abs(diffGcoY))
        meanDiffGcoZ = np.mean(np.abs(diffGcoZ))
        # 均方值
        rmsAccX = np.sqrt(np.mean(accX**2))
        rmsAccY = np.sqrt(np.mean(accY**2))
        rmsAccZ = np.sqrt(np.mean(accZ**2))
        rmsAcc = np.sqrt(np.mean(acc**2))
        rmsGcoX = np.sqrt(np.mean(gcoX**2))
        rmsGcoY = np.sqrt(np.mean(gcoY**2))
        rmsGcoZ = np.sqrt(np.mean(gcoZ**2))
        # 积分
        integralAccX = np.sum(accX) * 1 / frq
        integralAccY = np.sum(accY) * 1 / frq
        integralAccZ = np.sum(accZ) * 1 / frq
        # 范围
        rangeAccX = np.max(accX) - np.min(accX)
        rangeAccY = np.max(accY) - np.min(accY)
        rangeGcoX = np.max(gcoX) - np.min(gcoX)
        rangeGcoY = np.max(gcoX) - np.min(gcoY)
        rangeGcoZ = np.max(gcoX) - np.min(gcoZ)
        # 过零率
        gcoXZCR = _ZCR(gcoX)
        gcoYZCR = _ZCR(gcoY)
        gcoZZCR = _ZCR(gcoZ)
        # 均值
        meanEmg1 = np.mean(emg1)
        meanEmg2 = np.mean(emg2)
        meanEmg3 = np.mean(emg3)
        meanEmg4 = np.mean(emg4)
        meanEmg5 = np.mean(emg5)
        meanEmg6 = np.mean(emg6)
        meanEmg7 = np.mean(emg7)
        meanEmg8 = np.mean(emg8)
        # 均方值
        rmsEmg1 = np.mean(emg1)
        rmsEmg2 = np.sqrt(np.mean(emg2**2))
        rmsEmg3 = np.sqrt(np.mean(emg3**2))
        rmsEmg4 = np.sqrt(np.mean(emg4**2))
        rmsEmg5 = np.sqrt(np.mean(emg5**2))
        rmsEmg6 = np.sqrt(np.mean(emg6**2))
        rmsEmg7 = np.sqrt(np.mean(emg7**2))
        rmsEmg8 = np.sqrt(np.mean(emg8**2))

        #要使用的特征
        feature.append(meanAccX)
        feature.append(meanAccY)
        feature.append(meanAccZ)
        feature.append(meanGcoX)
        feature.append(meanGcoY)
        feature.append(meanGcoZ)
        feature.append(rmsAccX)
        feature.append(rmsAccY)
        feature.append(rmsAccZ)
        feature.append(rmsGcoX)
        feature.append(rmsGcoY)
        feature.append(rmsGcoZ)
        feature.append(integralAccX)
        feature.append(integralAccY)
        feature.append(integralAccZ)
        feature.append(rangeAccX)
        feature.append(rangeAccY)
        feature.append(rangeGcoX)
        feature.append(rangeGcoY)
        feature.append(rangeGcoZ)
        # feature.append(meanDiffAccX);feature.append(meanDiffAccY);feature.append(meanDiffAccZ)
        # feature.append(meanDiffGcoX);feature.append(meanDiffGcoY);feature.append(meanDiffGcoZ)
        feature.append(gcoXZCR)
        feature.append(gcoYZCR)
        feature.append(gcoZZCR)
        feature.append(meanEmg1)
        feature.append(meanEmg2)
        feature.append(meanEmg3)
        feature.append(meanEmg4)
        feature.append(meanEmg5)
        feature.append(meanEmg6)
        feature.append(meanEmg7)
        feature.append(meanEmg8)
        feature.append(rmsEmg1)
        feature.append(rmsEmg2)
        feature.append(rmsEmg3)
        feature.append(rmsEmg4)
        feature.append(rmsEmg5)
        feature.append(rmsEmg6)
        feature.append(rmsEmg7)
        feature.append(rmsEmg8)
    return feature


def featureGetTwo(emgDataRightAll, imuDataRightAll, emgDataLeftAll, imuDataLeftAll, divisorRight=8, divisorLeft=4):
    """
    对双手运动的手势特征进行提取，理论上应该做数据融合处理，这里是直接拆分成两个独立的数据流分别提取特征组合当做双手手势运动的特征
    数据格式列表或者数组都可以
    :param emgDataRightAll:右手的emg数据
    :param imuDataRightAll:右手的imu数据
    :param emgDataLeftAll:左手的emg数据
    :param imuDataLeftAll:左手的imu数据
    :param divisorRight:右手数据流的分片数
    :param divisorLeft:左手数据流的分片数
    :return:双手手势运动的特征
    """
    featureRight = featureGet(emgDataRightAll, imuDataRightAll, divisorRight)
    featureLeft = featureGet(emgDataLeftAll, imuDataLeftAll, divisorLeft)
    featureAll = featureRight + featureLeft
    if len(featureAll) == 312:
        print('featureGetTwoError')
    return featureAll


def saveExcleTwoDimension(file='new.xls', dataArray=[], index=0):
    """
    将二维数据存储到excle表格中
    :param file:文件名
    :param dataArray:数据
    :param index:行偏置
    :return: 生成一个excle表格，返回当前excle表格的最后一行的行数
    """
    # index是行偏置
    book = xlwt.Workbook()  # 创建一个Excel
    sheet1 = book.add_sheet('hello')  # 在其中创建一个名为hello的sheet
    for i in range(len(dataArray)):  # 行数
        for j in range(len(dataArray[i])):  # 列数
            sheet1.write(i + index, j, float(dataArray[i][j]))
    book.save(file)  # 创建保存文件
    return index + len(dataArray)


# def saveExcle(file='new.xls', dataArray=[], dimensions=2):
#     """
#
#     :param file:
#     :param dataArray:
#     :param dimensions:
#     :return:
#     """
#     index = 0
#     if dimensions == 2:
#         saveExcleTwoDimension(file, dataArray)
#     else:
#         # 此时只考虑三维
#         dataNumber = len(dataArray[0])
#         for i in range(dataNumber):
#             index = saveExcleTwoDimension(file, dataArray[i], index)


import xlrd
#


def excelToDict(file, by_name=u'Sheet1'):
    """
    获取Excel表格中的数据,并将其转换成字典。
    第一列为字典key，第二类为字典value
    :param file: 文件
    :param by_name: Sheet1名称
    :return:返回一个字典
    """
    data = xlrd.open_workbook(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows
    dict = {}
    for rownum in range(0, nrows):
        row = table.row_values(rownum)
        if row:
            keyName = int(row[0])
            value = row[1]
            if isinstance(value, float):
                value = int(value)
            dict[keyName] = value
    return dict


class DataCache(object):
    """
    实现一个数据的缓存池，缓存深度100
    用于缓存手语识别的结果

    """

    def __init__(self, maxCacheSize=100):
        """Constructor"""
        self.cache = []
        self.max_cache_size = maxCacheSize
        self.cacheLength = 0

    def getCache(self):
        """
        根据该键是否存在于缓存当中返回True或者False
        """
        return self.cache

    def update(self, string):
        """
        更新该缓存
        """
        if self.cacheLength > self.max_cache_size:
            print('cache is full')
            return False

        self.cache.append(string)
        self.cacheLength = self.cacheLength + 1

    def delete(self):
        """
        删除具备最早访问日期的输入数据
        """
        if self.cacheLength == 0:
            print('Null')
        else:
            self.cache.pop()
            self.cacheLength = self.cacheLength - 1

    @property
    def size(self):
        """
        返回缓存容量大小
        """
        return self.cacheLength

    def clear(self):
        self.cache = []
        self.cacheLength = 0


def normalized(gestureEmg, gestureImu):
    """
    对数据归一化
    :param gestureEmg:  手语运动的肌电流数据
    :param gestureEmg:  手语运动的惯性传感器数据
    :return:  归一化数据的肌电流，惯性传感器数据
    """
    gestureEmg = np.array(gestureEmg)
    gestureImu = np.array(gestureImu)
    emgMax = np.max(np.max(gestureEmg))
    imuMax = np.max(np.max(gestureImu))
    imuMin = np.min(np.min(gestureImu))
    emgData = (gestureEmg) / emgMax
    imuData = (gestureImu - imuMin) / (imuMax - imuMin)
    return emgData, imuData


def getMatFeature(file):
    """
    对mat数据进行特征提取，主要是前期的数据是在matlab进行数据分析和分割，然后在python环境下训练，所以需要该函数
    当把数据的分析和分割用python实现后，也就是利用getDataSet可以实现数据集的扩充之后，这个功能便基本不再。唯一的使用情况是清空了python下的获取的全部数据，重新从导入mat数据情况下才会使用
    mat数据结构
        包含结构体w
        w包含四个数据，emgData imuData len以及 lables
        nonZeoLabel是非0数组下标，row是非0数据行数
        读取数据
    :param file:文件位置
    :return: 特征和标签
    """
    data = scio.loadmat(file)
    featureOne = []
    featureTwo = []
    w = data['data']
    dataType = w['dataType']
    dataType = dataType[0, 0]
    dataType = dataType[0, 0]
    if dataType == 2:
        emgRight = w['emgRight']
        imuRight = w['imuRight']
        emgRight = emgRight[0, 0]
        imuRight = imuRight[0, 0]
        emgLeft = w['emgLeft']
        imuLeft = w['imuLeft']
        emgLeft = emgLeft[0, 0]
        imuLeft = imuLeft[0, 0]
        labels = w['Lable']
        labels = labels[0, 0]
        len = w['len']
        len = len[0, 0]
        len = len[0, 0]
        row = len
        emgLeft = emgLeft[0:row, :]
        imuLeft = imuLeft[0:row, :]
        emgLeft, imuLeft = normalized(emgLeft, imuLeft)
    else:
        emgRight = w['emgData']
        imuRight = w['imuData']
        emgRight = emgRight[0, 0]
        imuRight = imuRight[0, 0]
        labels = w['lables']
        labels = labels[0, 0]
        len = w['len']
        len = len[0, 0]
        len = len[0, 0]
        row = len * 5
        # 只有一只手的数据，那就将左手设定为0
        emgLeft = 0
        imuLeft = 0
    emgRight = emgRight[0:row, :]
    imuRight = imuRight[0:row, :]

    # 归一化
    emgRight, imuRight = normalized(emgRight, imuRight)
    if dataType == 1:
        featureOne = featureGet(emgRight, imuRight, divisor=8)

    elif dataType == 2:
        featureTwo = featureGetTwo(emgRight, imuRight, emgLeft, imuLeft, divisorRight=8, divisorLeft=4)
    if featureOne == []:
        return featureTwo, labels
    else:
        return featureOne, labels


def getKNN(trainX, trainY):
    """
    训练KNN模型
    :param trainX: 特征
    :param trainY: 标签
    :return: KNN模型
    """
    from sklearn.neighbors import KNeighborsClassifier as knn
    trainX = np.array(trainX)
    trainY = np.array(trainY)
    model = knn(n_neighbors=1, weights='distance')
    model.fit(trainX, trainY.ravel())
    return model


def getSVM(trainX, trainY):
    """
    训练SVM模型
    :param trainX: 特征
    :param trainY: 标签
    :return: SVM模型
    """
    from sklearn.svm import SVC
    trainX = np.array(trainX)
    trainY = np.array(trainY)
    model = SVC(kernel='linear', degree=3)
    model.fit(trainX, trainY.ravel())
    return model


def getModel(feature, label, ratio):
    """
    对输入数据进行训练和验证
    :param feature: 数据特征
    :param label: 数据标签，维度要和特征一直
    :param ratio: 用于测试的数据比例
    :return: 训练模型和准确度
    """

    " ""初始化 """
    length = len(feature)
    """模型训练"""
    model = getSVM(feature, label)
    """测试模型准确度"""
    """获取测试数据，训练数据"""
    learnLabel = []
    learnIndex = []
    number = int(length * (1 - ratio))
    learnData = random.sample(feature, number)
    for i in learnData:
        learnIndex.append(feature.index(i))
    learnIndex = tuple(learnIndex)
    allIndex = tuple(range(len(feature)))
    testIndex = set(allIndex).difference(set(learnIndex))
    for i in learnIndex:
        learnLabel.append(label[i])

    learnModel = getSVM(learnData, learnLabel)

    right = 0
    for i in testIndex:
        testData = feature[i]
        testLabel = label[i]
        testResult = learnModel.predict([testData])
        if testResult == testLabel:
            right = right + 1
    accuracy = right / len(testIndex)
    return model, accuracy


def getNpyData(featureName='', labelName=''):
    """
    读取存储的数据集
    :param featureName:存储特征的文件名
    :param labelName:存储标签的文件名
    :return:特征和标签
    """

    feature = np.load(featureName)
    feature = list(feature)
    feature.pop(len(feature) - 1)

    label = np.load(labelName)
    label = list(label)
    label.pop(len(label) - 1)
    return feature, label


def saveNpyDataOne(featureData=None, labelData=None, flag=2):
    '''
    对数单手手势的的数据集进行存储

    :param featureData: 传入特征值list
    :param labelData: 传入标签list
    :param flag: 标签值，1是存储原始数据，2是存储缓存数据，默认为2
    :return: 无返回值，直接存储数据
    '''
    featureData = featureData + [0]
    np.array(featureData)
    if flag == 1:
        np.save('oneFeature', featureData)
    elif flag == 2:
        np.save('oneFeatureCache', featureData)
    else:
        print('error save flag')
    labelData = labelData + [0]
    np.array(labelData)
    if flag == 1:
        np.save('oneLabel', labelData)
    elif flag == 2:
        np.save('oneLabelCache', labelData)
    else:
        print('error save flag')


def saveNpyDataTwo(featureData=None, labelData=None, flag=2):
    """
    对双手手势的数据集进行存储

    :param featureData: 传入特征值list
    :param labelData: 传入标签list
    :param flag: 标签值，1是存储为原始数据，2是存储为缓存数据，默认为2
    :return: 无返回值，直接存储数据
    """

    featureData = featureData + [0]
    np.array(featureData)
    if flag == 1:
        np.save('twoFeature', featureData)
    elif flag == 2:
        np.save('twoFeatureCache', featureData)
    else:
        print('error save flag')
    labelData = labelData + [0]
    np.array(labelData)
    if flag == 1:
        np.save('twoLabel', labelData)
    elif flag == 2:
        np.save('twoLabelCache', labelData)
    else:
        print('error save flag')


def getFloderNumber(path=None):
    """
    获取文件夹下文件夹数目
    :param path: 文件夹路径
    :return: 当前路径下文件夹数目
    """
    count = 0
    floderExist = os.path.exists(path)
    if floderExist:
        for fn in os.listdir(path):  # fn 表示的是文件名
            count = count + 1
    return count


if __name__ == '__main__':
    cache = DataCache()
    cache.update('你好')
    cache.delete()
    print(cache.getCache())