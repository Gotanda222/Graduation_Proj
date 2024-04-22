from scipy.signal import fftconvolve


import numpy as np
import scipy.signal


# 示例：计算环形6麦克风阵列中所有麦克风对的GCC-PHAT,the output is the input of the netowork

# 检查输出长度是否为51
def gcc_phat(sig1, sig2, fs, max_tau=None, interp=1):
    """
    计算两个信号之间的广义互相关-相位变换(GCC-PHAT)
    :param sig1: 信号1
    :param sig2: 信号2
    :param fs: 采样频率
    :param max_tau: 最大时间延迟
    :param interp: 插值因子，用于提高时间分辨率
    :return: 延迟估计的中心51个样本
    """
    # 傅里叶变换
    n = sig1.size + sig2.size
    # Zero padding和插值因子提高分辨率
    n *= interp
    f1 = np.fft.rfft(sig1, n=n)
    f2 = np.fft.rfft(sig2, n=n)
    # GCC-PHAT计算
    gcc = f1 * np.conj(f2)
    gcc = gcc / (np.abs(gcc) + 1e-8)  # 避免除以零
    gcc = np.fft.irfft(gcc, n=n)
    # 循环移动结果使得零延迟对应中心
    gcc = np.roll(gcc, -gcc.size // 2)
    # 选择中心51个样本
    center_index = gcc.size // 2
    gcc_centered = gcc[center_index - 25:center_index + 26]  # 包含中心点，向两侧各取25个样本
    return gcc_centered
def calculate_gcc_features(mic_signals, fs):
    """
    计算环形6麦克风阵列的所有麦克风对GCC-PHAT特征
    :param mic_signals: 包含6个麦克风信号的列表
    :param fs: 采样频率
    :return: GCC特征字典
    """
    num_mics = len(mic_signals)
    gcc_features = {}
    for i in range(num_mics):
        for j in range(i+1, num_mics):
            gcc_name = f"gcc_{i+1}_{j+1}"
            gcc_features[gcc_name] = gcc_phat(mic_signals[i], mic_signals[j],fs)
    return gcc_features


# 生成一些示例数据
np.random.seed(0)
fs = 16000  # 采样频率16kHz
t = np.linspace(0, 1, fs, endpoint=False)
mic_signals = [np.sin(2 * np.pi * 440 * t + np.random.uniform(0, 2*np.pi)) for _ in range(6)]

# 计算并打印GCC-PHAT特征
gcc_features = calculate_gcc_features(mic_signals, fs)
print(len(gcc_features))
for name, gcc in gcc_features.items():
    print(name, len(gcc))  # 打印每对麦克风的GCC-PHAT峰值




