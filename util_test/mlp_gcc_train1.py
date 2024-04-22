from models.mlp_gcc_generate import build_mlp_gcc_model 
# 训练模型
input_shape = (51 * 6,)
model = build_mlp_gcc_model(input_shape)
history = model.fit(
    x_train, y_train,
    epochs=50,
    batch_size=32,
    validation_data=(x_val, y_val),
    verbose=1
)

# 评估模型
test_loss = model.evaluate(x_test, y_test, verbose=1)
print("Test loss:", test_loss)

# 模型预测
predictions = model.predict(x_test)
