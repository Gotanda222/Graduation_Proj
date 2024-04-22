import numpy as np
import soundfile as sf
import os

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

# 处理声源信号并生成多通道输出
angles = np.linspace(0, 360, 360, endpoint=False)
distances = [0.5, 1, 1.5]

for angle in angles:
    for distance in distances:
        filename = f'voice_angle_{int(angle)}_dist_{distance:.1f}.wav'
        file_path = os.path.join(input_folder, filename)
        source_signal, _ = sf.read(file_path)
        multi_channel_signals = np.zeros((len(source_signal), num_mics))

        # 声源位置
        source_x = distance * np.cos(np.radians(angle))
        source_y = distance * np.sin(np.radians(angle))

        # 计算并叠加每个麦克风的信号
        for i, (mic_x, mic_y) in enumerate(mic_positions):
            mic_dist = np.sqrt((mic_x - source_x) ** 2 + (mic_y - source_y) ** 2)
            delay = int((mic_dist / sound_speed) * sampling_rate)
            attenuation = 1 / (1 + mic_dist)

            # 计算延迟信号并应用衰减
            if delay < len(source_signal):
                multi_channel_signals[delay:, i] = source_signal[:-delay] * attenuation

        # 保存6通道信号到一个文件
        output_filename = f'signals_angle_{int(angle)}_dist_{distance:.1f}.wav'
        output_file_path = os.path.join(output_folder, output_filename)
        sf.write(output_file_path, multi_channel_signals, samplerate=sampling_rate)

print("All multi-channel microphone signals processed and saved.")
