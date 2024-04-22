import numpy as np

def simulate_mic_array_capture_multiple_sources(audio_signals, source_angles, mic_array_radius, fs=44100):
    """
    模拟环形六麦克风阵列采集多个声源的音频信号。

    参数:
    - audio_signals: 各个声源的音频信号列表，每个元素是一个NumPy数组。
    - source_angles: 各声源的角度（度），每个元素相对于正北方向的角度。
    - mic_array_radius: 麦克风阵列的半径（米）。
    - fs: 采样率（赫兹），默认为44100Hz。

    返回:
    - mic_signals: 六通道的音频信号，每个通道代表一个麦克风的输出。
    """
    speed_of_sound = 343  # 声速（m/s）
    num_mics = 6
    mic_angles = np.linspace(0, 360, num_mics, endpoint=False)  # 计算六个麦克风的角度位置
    mic_angles_rad = np.deg2rad(mic_angles)

    # 计算可能的最大延迟以适当初始化mic_signals
    max_signal_length = max([len(sig) for sig in audio_signals])
    max_delay = mic_array_radius / speed_of_sound * fs  # 最大理论延迟
    mic_signals = np.zeros((num_mics, int(max_signal_length + max_delay)))

    for audio_signal, source_angle in zip(audio_signals, source_angles):
        source_angle_rad = np.deg2rad(source_angle)
        delays = mic_array_radius * (np.cos(mic_angles_rad - source_angle_rad) / speed_of_sound)
        sample_delays = np.round(fs * delays).astype(int)
        min_delay = np.min(sample_delays)
        sample_delays -= min_delay  # 将所有延迟调整为非负

        # 对每个麦克风应用延迟
        for i in range(num_mics):
            delay = sample_delays[i]
            end_index = delay + len(audio_signal)
            end_index = min(end_index, mic_signals.shape[1])  # 确保不超过数组边界
            mic_signals[i, delay:end_index] += audio_signal[:end_index - delay]

    return mic_signals

# 示例用法
audio_signals = [np.random.normal(0, 1, 44100), np.random.normal(0, 1, 44100)]  # 两个声源的示例音频信号
source_angles = [45, 135]  # 两个声源的角度
mic_array_radius = 0.1  # 麦克风阵列半径

# 调用函数
mic_signals = simulate_mic_array_capture_multiple_sources(audio_signals, source_angles, mic_array_radius, fs=44100)
print(mic_signals.shape)  # 查看输出信号的形状
