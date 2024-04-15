import numpy as np
import matplotlib.pyplot as plt

# 定义参数
sound_speed = 343       # 声速，单位：米/秒
sampling_rate = 44100   # 采样率，单位：Hz
duration = 2            # 信号持续时间，单位：秒
base_frequency = 200    # 人声基本频率
num_mics = 6            # 麦克风数量
radius = 0.1            # 环形麦克风阵列的半径，单位：米
source_position = np.array([0, 1])  # 声源位置，单位：米

# 创建时间数组
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 计算麦克风位置
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
mic_positions = np.vstack((radius * np.cos(theta), radius * np.sin(theta))).T

# 计算从声源到每个麦克风的距离
distances = np.sqrt(((mic_positions - source_position)**2).sum(axis=1))

# 生成每个麦克风的信号
signals = np.zeros((len(t), num_mics))
noise_level = 0.05  # 噪声水平
for i in range(num_mics):
    delay = distances[i] / sound_speed
    delayed_t = t - delay
    # 计算衰减因子
    attenuation = 1 / (1 + distances[i])
    # 生成人声信号模型，包含多个谐波
    voice_signal = np.sum([np.sin(2 * np.pi * (base_frequency * (n + 1)) * delayed_t) for n in range(3)], axis=0)
    # 应用衰减和随机噪声
    signals[:, i] = attenuation * voice_signal * (delayed_t >= 0) + noise_level * np.random.randn(len(t))

# 绘制所有麦克风的信号
plt.figure(figsize=(10, 12))
for i in range(num_mics):
    ax = plt.subplot(num_mics, 1, i + 1)
    ax.plot(t, signals[:, i])
    ax.set_title(f'Signal at Microphone {i+1}')
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Amplitude')
    if i < num_mics - 1:
        ax.set_xticklabels([])
plt.tight_layout()
plt.show()

# 绘制麦克风阵列的几何形状
plt.figure()
plt.scatter(mic_positions[:, 0], mic_positions[:, 1], color='red', label='Microphones')
plt.scatter(source_position[0], source_position[1], color='blue', label='Source')
plt.legend()
plt.title('Microphone Array Geometry')
plt.xlabel('X Position (meters)')
plt.ylabel('Y Position (meters)')
plt.axis('equal')
plt.grid(True)
plt.show()
