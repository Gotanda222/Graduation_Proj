import numpy as np
import os
import soundfile as sf  # 使用soundfile库来保存音频文件

# 创建保存音频文件的文件夹
output_folder = 'voice_signals'
os.makedirs(output_folder, exist_ok=True)

# 定义参数
sampling_rate = 44100  # 采样率，单位：Hz
duration = 2           # 信号持续时间，单位：秒
base_frequency = 200   # 基础频率，模拟人声的基频

# 创建时间数组
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
# 定义声源位置和距离
angles = np.linspace(0, 360, 360, endpoint=False)  # 360个方向
distances = [0.5, 1, 1.5]  # 三个距离

# 生成并保存信号
for angle in angles:
    for distance in distances:
        # 生成包含多个谐波的人声信号
        voice_signal = np.sin(2 * np.pi * base_frequency * t)  # 基频
        harmonics = [2, 3, 4, 5]  # 谐波系数
        for n in harmonics:
            voice_signal += np.sin(2 * np.pi * base_frequency * n * t) / n
        
        # 标准化信号
        voice_signal /= np.max(np.abs(voice_signal))

        # 命名并保存文件
        filename = f'voice_angle_{int(angle)}_dist_{distance:.1f}.wav'
        file_path = os.path.join(output_folder, filename)
        sf.write(file_path, voice_signal, samplerate=sampling_rate)

print("All voice signals generated and saved.")

#在刚刚生成的1080个声源信号的基础上，要求生成6通道信号模拟真实环境中环形麦克风阵列收到的信号
