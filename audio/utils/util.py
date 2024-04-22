from pydub import AudioSegment
import os
from scipy.signal import resample
import shutil
import wave
from pydub import AudioSegment


directory = '/home/zrh/BS/project/audio'  # 这里填写你的文件夹路径
source_folder = "/home/zrh/BS/CNN_DOA/DATASETS/TIMIT"
destination_folder = "/home/zrh/BS/dataset/TIMIT"
input_file_path = '/home/zrh/BS/dataset/TIMIT'  # 输入文件路径
output_file_path = '/home/zrh/BS/dataset/TIMIT_AMPLIFIED'  # 输出文件路径

def rename_wav_files(directory, prefix='file_'):
    """
    批量重命名目录中的所有WAV文件。

    :param directory: 包含WAV文件的目录。
    :param prefix: 新文件名的前缀。
    """
    # 获取目录中所有WAV文件
    files = [f for f in os.listdir(directory) if f.endswith(')')]
    # 排序文件，确保命名顺序
    files.sort()

    # 遍历文件并重命名
    for index, file in enumerate(files):
        new_name = f"{prefix}{index + 1:03d}.wav"  # 生成新文件名，如 file_001.wav
        old_path = os.path.join(directory, file)
        new_path = os.path.join(directory, new_name)
        os.rename(old_path, new_path)  # 重命名文件
        print(f'Renamed "{file}" to "{new_name}"')


def extract_wav_files(source_dir, target_dir):
    # 遍历源目录及其子目录
    for root, dirs, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith('.wav'):
                filepath = os.path.join(root, filename)
                # 如果文件名以"SI"或"SX"开头，则复制到目标文件夹中
                if filename.startswith('SI') or filename.startswith('SX'):
                    target_file = os.path.join(target_dir, filename)
                    shutil.copyfile(filepath, target_file)
                    print(f"已提取文件：{filename} -> {target_file}")
#
def process_wav_files(directory, target_sample_rate=16000, target_length=8192):
    """
    批量处理目录中的WAV文件：转换采样率到16kHz，调整长度到8192个样本点。

    :param directory: 包含WAV文件的目录。
    :param target_sample_rate: 目标采样率。
    :param target_length: 目标样本点数。
    """
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            file_path = os.path.join(directory, filename)
            audio = AudioSegment.from_wav(file_path)

            # 检查采样率
            if audio.frame_rate == 48000:
                # 转换采样率
                audio = audio.set_frame_rate(target_sample_rate)

                # 转换为样本数组
                samples = audio.get_array_of_samples()

                # 重新采样至目标样本长度
                if len(samples) != target_length:
                    samples = resample(samples, target_length)

                # 从新的样本数组创建音频段
                new_audio = audio._spawn(samples.tobytes())

                # 保存修改后的文件
                new_file_path = os.path.join(directory, f"processed_{filename}")
                new_audio.export(new_file_path, format='wav')
                print(f'Processed and saved "{new_file_path}"')

def delete_wav_files(directory):
    # 遍历目录下的文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # 如果文件名包含.WAV，则删除该文件
        if filename.lower().endswith('V'):
            os.remove(filepath)
            # if 'WAV' in filename:
            #     os.remove(filepath)
            #     print(f"已删除文件：{filename}")
def count_files(directory):
    # 初始化文件计数器
    file_count = 0
    # 遍历目录下的文件
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        # 如果是文件而不是目录，则增加计数器
        if os.path.isfile(filepath):
            file_count += 1
    return file_count

def is_valid_wav(file_path):
    try:
        # 尝试打开WAV文件
        with wave.open(file_path, 'rb') as wf:
            # 检查文件头是否以"RIFF"开头
            if wf.getnframes() > 0:
                return True
            else:
                return False
    except wave.Error:
        return False
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

def delete_invalid_wav_files(directory):
    invalid_files = []
    # 遍历目录下的文件
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # 检查文件是否是WAV格式并且符合RIFF格式
        if filename.lower().endswith('.wav') and not is_valid_wav(file_path):
            # 删除不符合条件的文件
            os.remove(file_path)
            invalid_files.append(file_path)
            print(f"Deleted invalid WAV file: {file_path}")
    return invalid_files
def increase_volume(input_file, output_file, gain_dB=20):
    for filename in os.listdir(input_file):
        file_path_input = os.path.join(input_file, filename)
        file_path_output = os.path.join(output_file, filename)
    # 加载WAV文件
        audio = AudioSegment.from_wav(file_path_input)

    # 调整音量大小
        audio = audio + gain_dB

    # 导出为新的WAV文件
        audio.export(file_path_output, format="wav")


# 示例用法：
# 指定输入和输出文件路径以及增益（以dB为单位）


# 调用函数提高音量
increase_volume(input_file_path, output_file_path)

# directory_path = '/path/to/your/directory'  # 更改为实际的目录路径

# invalid_files = delete_invalid_wav_files(directory)

# print(f"Deleted {len(invalid_files)} invalid WAV files.")


# rename_wav_files(directory)

# process_wav_files(directory)

# extract_wav_files(source_folder, destination_folder)
#
# delete_wav_files(destination_folder)
#
# num_files = count_files(destination_folder)
# print(f"文件夹中文件的数量为：{num_files}")
