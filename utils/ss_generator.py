import numpy as np
import matplotlib.pyplot as plt
import os
import soundfile as sf

# 定义参数
sound_speed = 343       # 声速，单位：米/秒
sampling_rate = 44100   # 采样率，单位：Hz
duration = 2            # 信号持续时间，单位：秒
base_frequency = 200    # 人声基本频率
num_mics = 6            # 麦克风数量
radius = 0.1            # 环形麦克风阵列的半径，单位：米

# 创建时间数组
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 计算麦克风位置
theta = np.linspace(0, 2 * np.pi, num_mics, endpoint=False)
mic_positions = np.vstack((radius * np.cos(theta), radius * np.sin(theta))).T

# 文件保存目录
folder_name = 'Generated_Signals'
os.makedirs(folder_name, exist_ok=True)

# 生成和保存信号
distances = [0.5, 1.0, 1.5]  # 定义源距离
angles = np.linspace(0, 360, 360, endpoint=False)  # 定义源方向角度

for angle in angles:
    radian = np.deg2rad(angle)
    for dist in distances:
        # 计算声源位置
        source_position = np.array([radius * np.cos(radian), radius * np.sin(radian)]) * dist
        for i in range(num_mics):
            # 计算从声源到麦克风的距离
            dist_to_mic = np.linalg.norm(mic_positions[i] - source_position)
            # 延迟
            delay = dist_to_mic / sound_speed
            delayed_t = t - delay
            # 生成信号
            signal = np.sin(2 * np.pi * base_frequency * delayed_t) * (delayed_t >= 0)
            # 文件命名和保存
            filename = f'Signal_Angle{int(angle)}_Dist{dist}_Mic{i+1}.wav'
            filepath = os.path.join(folder_name, filename)
            sf.write(filepath, signal, sampling_rate)

print("All signals generated and saved.")
