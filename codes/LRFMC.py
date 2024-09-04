######## 构建 LRFMC模型 ########
import pandas as pd
from sklearn.preprocessing import StandardScaler

from log import *

class LRFMC:
    def __init__(self):
        self.log = Log()
        return
    def getFeatures(self,airline):
        # 选取需求特征
        airline_selection = airline[["FFP_DATE","LOAD_TIME",
                                     "FLIGHT_COUNT","LAST_TO_END",
                                     "avg_discount","SEG_KM_SUM"]]
        # 构建L特征
        L = pd.to_datetime(airline_selection["LOAD_TIME"]) \
            - pd.to_datetime(airline_selection["FFP_DATE"])
        self.log(LOG_DEBUG,"\n",L[:5])  #测试前五行
        # 转成月份
        L = L.astype("str").str.split().str[0]
        L = L.astype("int")/30

        #合并特征
        airline_features = pd.concat([L,
                airline_selection.iloc[:,2:]],axis = 1)  #axis=1使函数按列合并,[:,2:]舍弃了原本的前两列
        airline_features =airline_features.rename(columns={0:"L"}) # 重命名没有名字的列
        self.log(LOG_DEBUG,"\n",airline_features.head())  #缺省参数为5，打印前五行
        return airline_features

    def storeStandData(self,airline_features):
        data = StandardScaler().fit_transform(airline_features)
        SDF = pd.DataFrame(data);  #获取 standardDataFrame(SDF)
        SDF = SDF.rename(columns={0:"L",1:"F",2:"R",3:"C",4:"M"})
        self.log(LOG_INFO,"标准化后的前五行的LRFMC五个特征为\n",SDF.head())
        SDF.to_excel("../tmp/airline_scale.xlsx")  ##储存值tmp文件夹


