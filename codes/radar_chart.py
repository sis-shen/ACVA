import matplotlib.pyplot as plt
import numpy as np

class RadarDrawer():
    def __init__(self):
        return

    def __call__(self, kmeans_moudel, n_clusters):
        plt.rc("font",family="Microsoft YaHei")
        # 标签
        labels = np.array([u'ZL',u'ZR',u'ZF',u'ZM',u'ZC'])

        plot_data = kmeans_moudel.cluster_centers_
        # 指定颜色
        color = ['b','g','r','c','y']
        # 计算雷达图的角度
        angles = np.linspace(0,2*np.pi,n_clusters,endpoint=False)

        # 闭合(首尾列相同) 并用np把pandas的DataFrame转成原生数组
        plot_data = np.concatenate((plot_data,plot_data[:,[0]]),axis = 1)
        angles_org = angles
        angles = np.concatenate((angles,[angles[0]]))

        fig = plt.figure(figsize=(6,6),dpi = 160)
        #polar参数
        ax = fig.add_subplot(111, polar=True)  # 设置坐标为极坐标
        # 画若干个五边形
        floor = np.floor(plot_data.min())   # 大于最小值的最大整数
        ceil = np.ceil(plot_data.max())     # 小于最小值的最小整数
        n = len(labels)
        for i in np.arange(floor,ceil+0.5, 0.5):
            ax.plot(angles,[i] *(n+1),'-.',lw=0.5,color='black')
        # 话不同客户群的分割线
        for i in range(len(plot_data)):
            ax.plot(angles,plot_data[i],color = color[i],
                    label='客户群'+str(i+1),linewidth=2, linestyle='-.')
        ax.set_rgrids(np.arange(0,2.5, 0.5))  # 画出每层的权重
        ax.set_thetagrids(angles_org* 180/np.pi,labels)  # 设置显示的角度为度数制
        plt.legend(loc='lower right',bbox_to_anchor=(1.1, -0.1))  #设置图例位置在画布外
        #plt.legend()

        #ax.set_theta_zero_location('N')         # 设置极坐标的起点（即0°）在正北方向
        ax.spines['polar'].set_visible(False)   # 不显示极坐标最外面的圈
        ax.grid(False)                          # 不显示默认分割线
        plt.savefig("../tmp/ACVA_img.png")      # 储存图像的临时文件
        plt.show()