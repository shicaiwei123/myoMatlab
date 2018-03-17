from getData.getData import *
from myoAnalysis import *
from voice.speech import xf_speech

#speaker = xf_speech()    # 在minnowboard板子上无需设置端口号，默认'/dev/ttyS4'
speaker = xf_speech('/dev/ttyUSB0')


#译码，将识别到的标签翻译成手势含义
def decode(label):
    label=int(label)
    dict=\
        {#称呼
         1:'大家',2:'你',3:'我',4:'他',5:'和',6:'同学',7:'朋友',8:'儿子',9:'女儿',10:'爸爸',
         11:'妈妈',12:'爷爷',13:'奶奶',14:'人',
         #时间
         31:'早上',32:'中午',33:'晚上',34:'年',
         #礼貌用语
         51:'请',52:'好',53:'对不起',54:'谢谢',55:'不用',56:'再见',
         #地点
         71:'去',72:'在',73:'到',74:'家',75:'火车站',76:'机场',77:'汽车站',
         #交通
         101:'坐',102:'火车',103:'飞机',104:'公交车',105:'大巴',106:'地铁',
         #证件
         121:'证',122:'身份',123:'学生',
         #疑问
         131:'问',132:'什么',133:'多少',134:'哪里',
         #数字
         141:0,142:1,143:2,144:3,145:4,146:5,147:6,148:7,149:8,150:9,
         151:10,152:20,153:30,154:40,155:50,156:60,157:70,158:80,159:90,
         160:100,161:200,162:300,163:400,164:500,165:600,166:700,167:800,168:900,
         #就餐
         191:'吃',192:'饭',193:'饮料',194:'啤酒',195:'果汁',196:'钱',
         #生活
         211:'手机',212:'钱包',213:'没有',214:'看见',
         #情绪
         231:'爱',232:'我爱你',233:'高兴',234:'危险',235:'误会',236:'想',237:'不要'
    }
    return dict[label]


#isSave取True时时存储数据，取False时时分析数据
if __name__ == '__main__':


    m = init()
    #shifoubaocunshuju
    isSave = False
    #导入模型

    #如果是存储数据
    if isSave:
        emgData=[]
        imuData=[]
        threshold=[]
        try:
            while True:
                emg, imu, emg_raw = getOnceData(m)
                emgData.append(emg)
                imuData.append(imu)
                E=engery(emg)
                threshold.append([E])
                if HAVE_PYGAME:
                   for ev in pygame.event.get():
                        if ev.type == QUIT or (ev.type == KEYDOWN and ev.unicode == 'q'):
                            testXlwt('emgData.xls', emgData)
                            testXlwt('imuData.xls', imuData)
                            testXlwt('emgRawData.xls', emg_raw)
                            testXlwt('threshold.xls', threshold)
                            raise KeyboardInterrupt()
                        elif ev.type == KEYDOWN:
                            if K_1 <= ev.key <= K_3:
                                m.vibrate(ev.key - K_0)
                            if K_KP1 <= ev.key <= K_KP3:
                                m.vibrate(ev.key - K_KP0)
        except KeyboardInterrupt:
            pass
        finally:
            m.disconnect()
    #否则是分析数据
    else:
        from sklearn.externals import joblib
        import threading
        import queue
        import time
        # 预测函数，用于多线程的回调
        #isFinsh 是线程锁
        isFinish=False
        def predict(model, data):
            t1=time.time()
            global isFinish
            result = model.predict(data)
            t2=time.time()
            isFinish=True
            out=decode(result)
            speaker.speech_sy(out)
            print(t2-t1)    #测试识别时间
            print(out)   #输出结果
            # return result

        threads = []
        model=joblib.load('KNN')
        emg=[]
        imu=[]
        fetureCache=queue.Queue(10)
        while True:
             emg,imu = getGestureData(m)
             if emg==10000:
                 break
             np.save('emg',emg)
             np.save('imu',imu)
             feture=fetureGet(emg,imu)
             fetureCache.put([feture])
             t1 = threading.Thread(target=predict, args=(model,fetureCache.get(),))
             # r=model.predict([feture])
             t1.start()
             # print(r)