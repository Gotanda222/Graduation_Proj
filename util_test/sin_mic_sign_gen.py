import numpy as np

def simulate_mic_array_capture(audio_signal, source_angle, mic_array_radius, fs=44100):
    """
    模拟环形六麦克风阵列采集声源的音频信号。

    参数:
    - audio_signal: 原始音频信号，一个NumPy数组。
    - source_angle: 声源的角度（度），相对于正北方向。
    - mic_array_radius: 麦克风阵列的半径（米）。
    - fs: 采样率（赫兹），默认为44100Hz。

    返回:
    - mic_signals: 六通道的音频信号，每个通道代表一个麦克风的输出。
    """
    speed_of_sound = 343  # 声速（m/s）
    num_mics = 6
    mic_angles = np.linspace(0, 360, num_mics, endpoint=False)  # 计算六个麦克风的角度位置

    # 转换角度为弧度
    source_angle_rad = np.deg2rad(source_angle)
    mic_angles_rad = np.deg2rad(mic_angles)

    # 计算每个麦克风与声源之间的距离差引起的延迟
    delays = mic_array_radius * (np.cos(mic_angles_rad - source_angle_rad) / speed_of_sound)

    # 将延迟转换为样本数
    sample_delays = np.round(fs * delays).astype(int)
    
    # 调整延迟，确保没有负值
    min_delay = np.min(sample_delays)
    sample_delays -= min_delay  # 将所有延迟调整为非负

    # 创建六通道音频信号数组，考虑最大延迟
    max_delay = np.max(sample_delays)
    mic_signals = np.zeros((num_mics, len(audio_signal) + max_delay))
    
    # 应用延迟到音频信号
    for i in range(num_mics):
        delay = sample_delays[i]
        mic_signals[i, delay:delay + len(audio_signal)] = audio_signal
    
    return mic_signals

# 示例用法
audio_signal = np.random.normal(0, 1, 44100)  # 生成一个秒长的音频信号作为示例
source_angle = 45  # 声源角度
mic_array_radius = 0.1  # 麦克风阵列半径

# 调用函数
mic_signals = simulate_mic_array_capture(audio_signal, source_angle, mic_array_radius, fs=44100)
print(mic_signals.shape)  # 查看输出信号的形状
