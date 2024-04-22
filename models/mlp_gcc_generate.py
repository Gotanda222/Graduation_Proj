import tensorflow as tf
from tensorflow.keras import layers, models

def build_mlp_gcc_model(input_shape):
    # 创建模型
    model = models.Sequential()
    
    # 第一个隐藏层，带ReLU激活和批量归一化
    model.add(layers.Dense(1000, input_shape=input_shape, activation='relu'))
    model.add(layers.BatchNormalization())
    
    # 第二个隐藏层
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.BatchNormalization())
    
    # 第三个隐藏层
    model.add(layers.Dense(1000, activation='relu'))
    model.add(layers.BatchNormalization())
    
    # 输出层，360个方向的可能性，使用sigmoid激活函数
    model.add(layers.Dense(360, activation='sigmoid'))
    
    # 编译模型，使用均方误差作为损失函数，优化器使用Adam
    model.compile(optimizer='adam', loss='mse')
    
    return model

# 假设输入特征的形状是（特征数,），例如使用一组GCC-PHAT特征
input_shape = (51 * 6,)  # 假设每个GCC-PHAT特征由51个时间延迟和6对麦克风组成

model = build_mlp_gcc_model(input_shape)

# 打印模型概况
model.summary()
