###### 实现日志系统 ########

# 定义日志等级
LOG_INFO = "Info"
LOG_ERROR = "Error"
LOG_WANING = "Warning"
LOG_FATAL = "Fatal"
LOG_DEBUG = "Debug"

class Log:
    def __init__(self):
        return

    def __call__(self,level,*msgs): # 重载()运算符
        print("[", level, "]",end='')
        for msg in msgs:
            print(msg)
        # 本项目与时间关系不大，日志系统不打印时间



