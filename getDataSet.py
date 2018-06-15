import getData.getData as myoData  # 数据接口
from myoAnalysis import saveExcle  # 数据操作
from myoAnalysis import excelToDict
import os
import xlrd


class DataFormal():
    """
    定义一个数据结构，可以生成相应文件信息传入到
     :param filename:   文件夹名字，手势名字，比如'你好'，默认为空
    :param handNumber: 手势中手的需要用到的手的数目，单手为1双手为2，默认单手
    :param dataNumber: 要采集的的手势的个数，为了防止误差，第一个和最后一个采集的手势会被去掉，该值的设定是要采集的数据量加2，总共，默认是12
    """

    def __init__(self, handNumber=1, fileName=None, dataNumber=12):
        self.__hand_number = handNumber
        self.__file_name = fileName
        self.__data_number = dataNumber

    def set_param(self, handNumber=1, fileName=None, dataNumber=12):
        self.__hand_number = handNumber
        self.__file_name = fileName
        self.__data_number = dataNumber


def getDataSet(HandNumber=1, FileName=None, DataNumber=12):

    # 初始化
    m = myoData.init()
    dataDict = excelToDict('dataSheet.xlsx')
    label = findLabel(dataDict,fileName)
    # 右手
    emgRightData = []  # 一次手势数据
    imuRightData = []  # 一次手势数据
    emgRightDataAll = []  # 所有数据
    imuRightDataAll = []
    # 左手
    emgLeftData = []  # 一次手势数据
    imuLeftData = []  # 一次手势数据
    emgLeftDataAll = []  # 所有数据
    imuLeftDataAll = []
    # 能量
    engeryDataAll = []  # 所有数据
    engeryDataSeg = []  # 一次手势数据
    gestureCounter = 0
    while True:
        emgRight, imuRight, emgRightAll, imuRightAll, \
            emgLeft, imuLeft, emgLeftAll, imuLeftAll, \
            engeryAll, engerySeg = myoData.getGestureData(m)

        gestureCounter = gestureCounter + 1
        print(gestureCounter)
        # if emgRight == 10000:
        if gestureCounter > DataNumber:
            engeryDataSeg = engeryDataSeg + [[gestureCounter - 1]]
            if HandNumber == 1:
                path = 'GuestData/one/' + FileName
                os.makedirs(path)
                saveExcle(path + '/emgDataRight.xls', emgRightData)
                saveExcle(path + '/imuDataRight.xls', imuRightData)
                saveExcle(path + '/emgDataRightAll.xls', emgRightDataAll)
                saveExcle(path + '/imuDataRightAll.xls', imuRightDataAll)

                saveExcle(path + '/engeryDataAll.xls', engeryDataAll)
                saveExcle(path + '/engeryDataSeg.xls', engeryDataSeg)
                saveExcle(path + '/label.xls', [label])

            elif HandNumber == 2:
                path = 'GuestData/two/' + FileName
                os.makedirs(path)
                saveExcle(path + '/emgDataRight.xls', emgRightData)
                saveExcle(path + '/imuDataRight.xls', imuRightData)
                saveExcle(path + '/emgDataRightAll.xls', emgRightDataAll)
                saveExcle(path + '/imuDataRightAll.xls', imuRightDataAll)

                saveExcle(path + '/emgDataLeft.xls', emgLeftData)
                saveExcle(path + '/imuDataLeft.xls', imuLeftData)
                saveExcle(path + '/emgDataLeftAll.xls', emgLeftDataAll)
                saveExcle(path + '/imuDataLeftAll.xls', imuLeftDataAll)

                saveExcle(path + '/engeryDataAll.xls', engeryDataAll)
                saveExcle(path + '/engeryDataSeg.xls', engeryDataSeg)
                saveExcle(path + '/label.xls', [label])
            else:
                print("error")
            break
            m.disconnect()
        #完善myo断开逻辑



        # 右手
        emgRightData = emgRightData + emgRight + [[0]]
        # print(emg)
        imuRightData = imuRightData + imuRight + [[0]]

        emgRightDataAll = emgRightDataAll + emgRightAll
        imuRightDataAll = imuRightDataAll + imuRightAll
        # 左手
        emgLeftData = emgLeftData + emgLeft + [[0]]
        # print(emg)
        imuLeftData = imuLeftData + imuLeft + [[0]]

        emgLeftDataAll = emgLeftDataAll + emgLeftAll
        imuLeftDataAll = imuLeftDataAll + imuLeftAll
        # 能量
        engeryDataAll = engeryDataAll + engeryAll
        engeryDataSeg = engeryDataSeg + engerySeg + [[0]]


def findLabel(dict=None,gestureName=None):
    keyList=[]
    valueList=[]
    for key,value in dict.items():
        keyList.append(key)
        valueList.append(value)
    if gestureName in valueList:
        valueIndex=valueList.index(gestureName)
        label=keyList[valueIndex]
    else:
        print("no gesture label")
    return label



if __name__ == '__main__':
    """
    获取数据
    """
    print("采集单手手势输入1，双手手势输入2：\t")
    handNumber = int(input())
    print("请输入要采集的手势名称：\t")
    fileName = input()
    print("请输入要采集手势的采集数目：\t")
    dataNumber = int(input())
    getDataSet(handNumber, fileName, dataNumber)
    print('hello world')
#lable单独保存，后面可能是存一次就训练，也可能采集多次再训练
#同一个手势采集了多次怎么办？
    #每一次采集建立一个文件夹，看有了几个文件夹，然后time1，time2或者加上日期，反正不会很多，不要考虑太多了，
    #
    #训练的时候遍历这些文件夹
    #用户可以选择删除这些文件夹，全部删除，选择删除，虽然我们应该提供更好哦的服务，让用户尽可能不去选择这个功能
    #训练的模型也可以保存，用户随意选择，加载的时候只从其中一个地方加载
    #可以恢复出厂设置
    #读数据，读取我们的和用户的，然后一起训练，我们的就是这样了，全部读入，用户也全部读入，然后训练，或者设置一个比例
    #接下来是文件操作，数据读取，训练，保存。
    #天，那还不如就直接做一个app设置。