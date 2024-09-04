import pandas as pd

class DataCleaner:
    def __init__(self):
        return
    def notNull(self,airline_data):  # 缺失值处理：去除票价为空的记录
        exp1 = airline_data["SUM_YR_1"].notnull()
        exp2 = airline_data["SUM_YR_2"].notnull()
        exp = exp1 & exp2  # 按位逻辑与,获取所需的布尔值列表
        #airline_notnull = airline_data.loc[exp, :]  # exp提供布尔值竖列表， ':'默认无参时，切片所有行,完成去除操作
        airline_notnull = airline_data[exp] #  这是上一句的简化写法（使用更多的缺省参数
        return airline_notnull

    def notOutlier(self,airline_data):
        index1 = airline_data["SUM_YR_1"].notnull()
        index2 = airline_data["SUM_YR_2"] != 0  # 效果和上一句的notnull()一样,都是生成bool array
        index3 = (airline_data["SEG_KM_SUM"] > 0) & \
                 (airline_data["avg_discount"] != 0)  # 折扣且总里程不为0的机票
        airline = airline_data[(index1 | index2) & index3]  # 丢弃票价为0，或折扣率为0，且总里程>0的异常值
        return airline
