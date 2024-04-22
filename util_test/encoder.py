import numpy as np
import matplotlib.pyplot as plt

#


def plot_doa_spectrum(doas, std_dev=10, amplitude=1):
    """
    绘制声源方向的空间频谱图。
    
    参数:
        doas: 声源角度的向量，每个元素表示一个声源的角度（单位为度）。
        std_dev: 高斯分布的标准差，默认为10。
        amplitude: 高斯分布的振幅，默认为1。
    """
    # 创建角度向量，用于空间频谱图的x轴（0度到360度）
    angles = np.linspace(0, 360, 360)
    
    # 初始化空间频谱图
    spectrum = np.zeros_like(angles, dtype=float)
    
    # 对每个声源，在空间频谱图上放置一个高斯分布
    for doa in doas:
        # 在空间频谱图上添加高斯分布
        spectrum += amplitude * np.exp(-0.5 * ((angles - doa) / std_dev) ** 2)
    
    # 绘制空间频谱图
    plt.figure(figsize=(10, 6))
    plt.plot(angles, spectrum)
    plt.title('Spatial Spectrum Plot')
    plt.xlabel('Angle (degrees)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# 示例用法
plot_doa_spectrum([30, 120])


def doa_spectrum(doas, std_dev=10, amplitude=1):
    
    angles = np.linspace(0, 360, 360)
    
    # 初始化空间频谱图
    spectrum = np.zeros_like(angles, dtype=float)
    
    # 对每个声源，在空间频谱图上放置一个高斯分布
    for doa in doas:
        # 在空间频谱图上添加高斯分布
        spectrum += amplitude * np.exp(-0.5 * ((angles - doa) / std_dev) ** 2)