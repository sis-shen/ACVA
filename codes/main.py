######### 主程序入口 #############
import pandas as pd
from sklearn.cluster import KMeans
import time

from log import *
from data_clean import *
from LRFMC import *
from radar_chart import  *

if __name__ == '__main__':

    log = Log()  # 实例化一个日志器
    data_cleaner = DataCleaner() #实例化数据清洗器
    LRFMCobj = LRFMC() # 实例化模型处理器

    # 从数据源获取数据
    airline_data = pd.read_csv("../data_raw/air_data.csv",
        encoding="gb18030")  # 导入航空数据
    log(LOG_INFO,'原始数据的形状为：', airline_data.shape)

    #数据预处理
    ## 缺失值处理：去除票价为空的记录
    airline_notnull = data_cleaner.notNull(airline_data)
    log(LOG_INFO,'删除缺失记录后数据的形状为：', airline_notnull.shape)

    ## 异常值处理: 只保留票价非零的，或者平均折扣率不为0且总飞行公里数大于0的记录。
    airline = data_cleaner.notOutlier(airline_notnull)
    log(LOG_INFO,'删除异常记录后数据的形状为：', airline.shape)

    # 构建LRFMC五大特征
    airline_features = LRFMCobj.getFeatures(airline)
    LRFMCobj.storeStandData(airline_features)

    # 获取KMeans对象
    ## 准备数据
    airline_scale = pd.read_excel("../tmp/airline_scale.xlsx")
    airline_scale = airline_scale.iloc[:,1:]  # 切掉第一列的作为行数标志的数字

    ## 对象实例化
    k = 5 ## 确定聚类中心数，这里我们预期聚类5类客户
    kmeans_model = KMeans(n_clusters=k,random_state=int(time.time()))  # 实例化对象
    kmeans_model = kmeans_model.fit(airline_scale)  # 用准备好的数据训练模型
    centers = kmeans_model.cluster_centers_
    log(LOG_INFO,"五个聚类中心为\n",centers)

    ## 统计不同类别样本的数目
    r1 = pd.Series(kmeans_model.labels_).value_counts()
    log(LOG_INFO,"最终每个类别的数目为\n",r1)

    # 作出图样
    RadarDrawer()(kmeans_model,n_clusters=k)
    log(LOG_INFO,"完成作图")
