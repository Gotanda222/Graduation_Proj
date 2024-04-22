import wave
import os

filename = "/home/zrh/BS/dataset/TIMIT/SI727.WAV"
directory= "/home/zrh/BS/dataset/TIMIT"
directory1= "/home/zrh/BS/dataset/TIMIT_AMPLIFIED"


def get_wav_properties(filename):
    # 打开 WAV 文件
    with wave.open(filename, 'rb') as wav_file:
        # 获取 WAV 文件的参数
        params = wav_file.getparams()
        num_channels = params.nchannels  # 声道数
        sample_width = params.sampwidth  # 采样宽度（字节）
        frame_rate = params.framerate     # 采样率
        num_frames = params.nframes        # 总帧数
        compression_type = params.comptype  # 压缩类型
        compression_name = params.compname  # 压缩名称

    # 打印 WAV 文件的参数
    print("Number of channels:", num_channels)
    print("Sample width (bytes per sample):", sample_width)
    print("Frame rate (samples per second):", frame_rate)
    print("Number of frames:", num_frames)
    print("Compression type:", compression_type)
    print("Compression name:", compression_name)

def get_wav_duration(wav_file):
    # 打开WAV文件
    with wave.open(wav_file, 'rb') as wf:
        # 获取帧数
        num_frames = wf.getnframes()
        # 获取采样率
        frame_rate = wf.getframerate()
        # 计算时长（秒）
        duration = num_frames / float(frame_rate)
        return duration


def get_all_wav_pro(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        get_wav_properties(filepath)


def get_all_wav_duration(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        duration_seconds = get_wav_duration(filepath)
        print(f"WAV文件时长为：{duration_seconds:.2f} 秒")


# get_all_wav_duration(directory)
get_all_wav_pro(directory)