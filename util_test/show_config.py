import numpy as np
import soundfile as sf
import os
import matplotlib.pyplot as plt

# 定义麦克风阵列和基本参数
num_mics = 6
radius = 0.1  # 麦克风阵列半径，单位：米
mic_positions = [(radius * np.cos(2 * np.pi * i / num_mics), radius * np.sin(2 * np.pi * i / num_mics)) for i in range(num_mics)]
sound_speed = 343  # 声速，单位：米/秒
sampling_rate = 44100  # 采样率，单位：Hz
duration = 2           # 信号持续时间，单位：秒
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 输入输出文件夹设置
input_folder = 'voice_signals'
output_folder = 'mic_received_signals'
os.makedirs(output_folder, exist_ok=True)

# 绘制麦克风阵列的形状和每个声源的位置
plt.figure(figsize=(8, 8))
for mic_x, mic_y in mic_positions:
    plt.scatter(mic_x, mic_y, color='blue', marker='o', s=100, label='Microphone')
plt.xlabel('X Position (meters)')
plt.ylabel('Y Position (meters)')
plt.title('Microphone Array Geometry')
plt.axis('equal')

angles = np.linspace(0, 360, 360, endpoint=False)
distances = [0.5, 1, 1.5]

for angle in angles:
    for distance in distances:
        # 声源位置
        source_x = distance * np.cos(np.radians(angle))
        source_y = distance * np.sin(np.radians(angle))
        plt.scatter(source_x, source_y, color='red', marker='o', s=50,label='Source')

plt.legend(['Microphone', 'Source'])
plt.show()
