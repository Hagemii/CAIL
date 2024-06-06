import matplotlib.pyplot as plt
import numpy as np

x = np.array([1,3, 5, 7, 9, 10, 11, 13, 15, 16, 17, 19, 19.5, 20])

# 不同种类的数据点
y_ptr = np.array([15,35, 45, 50, 51, 50, 51, 51, 50, 51, 51, 52, 52, 52.5])
y_typ_marker = np.array([4, 15,32, 44, 42, 43, 42, 44, 44, 43, 44, 45, 45, 46])
y_ent_marker = np.array([3, 14,33, 43, 45, 45, 46, 44, 45, 45, 46, 46, 46.5, 47])

# 画图
plt.plot(x, y_ptr, label='JRP')
plt.plot(x, y_typ_marker, label='ENT MARKER')
plt.plot(x, y_ent_marker, label='TYP MARKER')

# 设置 x 轴的标签
plt.xlabel('Training Epochs')
# 设置 y 轴的标签
plt.ylabel('F1-scores(%)')

# 设置 x 轴的刻度
plt.xticks([0,5,10,15,20])

# 创建图例
plt.legend()
# 保存图像
plt.savefig('chart.png')

# 显示图像
plt.show()
