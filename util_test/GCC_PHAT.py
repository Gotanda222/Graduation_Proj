import numpy as np
from scipy.signal import fftconvolve

def gcc_phat(sig1, sig2, fs, max_tau=None, interp=1):
    """
    该函数计算两个信号之间的GCC-PHAT互相关，并找到最大互相关的时间延迟。

    参数:
    sig1, sig2: 输入的两个信号
    fs: 采样频率
    max_tau: 允许的最大时间延迟，默认为None，表示由信号长度决定
    interp: 插值因子，用于提高互相关峰值检测的精度

    返回:
    tau: 估计的时间延迟
    cc: 归一化的互相关函数
    """
    # 确保两个信号长度相同
    n = sig1.shape[0]
    if sig2.shape[0] != n:
        raise ValueError("两个信号的长度必须相同")

    # 计算FFT
    SIG1 = np.fft.fft(sig1, n=n*interp)
    SIG2 = np.fft.fft(sig2, n=n*interp)
    
    # GCC-PHAT处理
    R = SIG1 * np.conj(SIG2)
    cc = np.fft.ifft(R / (np.abs(R) + 1e-15))
    cc = np.fft.fftshift(cc) / np.abs(cc).max()

    # 计算时间延迟
    max_shift = int(n * interp / 2)
    if max_tau:
        max_shift = np.minimum(int(max_tau * fs * interp), max_shift)

    cc = np.abs(cc)
    shift = np.argmax(cc)
    tau = (shift - max_shift) / (fs * interp)

    return tau, cc

# 例子: 使用随机信号测试GCC-PHAT
fs = 8000  # 采样率
t = np.arange(0, 1.0, 1/fs)
sig1 = np.sin(2*np.pi*440*t)  # 生成440 Hz的正弦波
sig2 = np.roll(sig1, int(0.0025*fs))  # 将sig1延迟2.5毫秒

# 计算时间延迟
tau, cc = gcc_phat(sig1, sig2, fs)
print(f"估计的时间延迟为：{tau:.6f} 秒")
