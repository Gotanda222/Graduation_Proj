import numpy as np
import matplotlib.pyplot as plt

# 设置声源的DOA（度），假设两个声源分别位于30度和120度
doas = [30, 120]

# 创建角度向量，用于空间频谱图的x轴（0度到360度）
angles = np.linspace(0, 360, 360)

# 初始化空间频谱图
spectrum = np.zeros_like(angles, dtype=float)

# 对每个声源，在空间频谱图上放置一个高斯分布
for doa in doas:
    # 高斯分布的参数
    mean = doa  # 均值，即声源的方向
    std_dev = 10  # 标准差，控制高斯分布的宽度
    amplitude = 1  # 高斯分布的振幅
    # 在空间频谱图上添加高斯分布
    spectrum += amplitude * np.exp(-0.5 * ((angles - mean) / std_dev) ** 2)

# 绘制空间频谱图
plt.figure(figsize=(10, 6))
plt.plot(angles, spectrum)
plt.title('sdf ')
plt.xlabel('角度（度）')
plt.ylabel('幅值')
plt.grid(True)
plt.show()
