import tensorflow as tf
from tensorflow.keras import layers, models


def create_tsnn_gccfb_model(input_shape):


    # 第一阶段：CNN
    cnn_input = layers.Input(shape=input_shape, name='cnn_input')
    x = layers.Conv2D(32, kernel_size=(3, 3), activation='relu')(cnn_input)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Conv2D(64, kernel_size=(3, 3), activation='relu')(x)
    x = layers.MaxPooling2D(pool_size=(2, 2))(x)
    x = layers.Flatten()(x)
    cnn_output = layers.Dense(128, activation='relu')(x)
    cnn_model = models.Model(inputs=cnn_input, outputs=cnn_output, name='cnn_stage')

    # 第二阶段：MLP
    mlp_input = layers.Input(shape=(128,), name='mlp_input')
    x = layers.Dense(128, activation='relu')(mlp_input)
    x = layers.Dense(64, activation='relu')(x)
    mlp_output = layers.Dense(10, activation='softmax')(x)  # 假设有10个方向类别
    mlp_model = models.Model(inputs=mlp_input, outputs=mlp_output, name='mlp_stage')

    # 将CNN和MLP串联起来
    combined_input = layers.Input(shape=input_shape)
    cnn_out = cnn_model(combined_input)
    tsnn_output = mlp_model(cnn_out)

    # 创建并编译模型
    model = models.Model(inputs=combined_input, outputs=tsnn_output, name='TSNN-GCCFB')
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    return model


# 假设输入数据的形状为(64, 64, 1)，例如64x64的GCCFB特征图
input_shape = (64, 64, 1)
model = create_tsnn_gccfb_model(input_shape)
model.summary()
