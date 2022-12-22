##手写字识别

————————


——————————

###大致架构
####神经网络
首先，主体的神经网络部分为采用tensorflow框架下的序列化接口的卷积神经网络，隐藏层代码如下
```python
    model = keras.models.Sequential([
        keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu, input_shape=(28, 28, 1)),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Dropout(0.2),
        keras.layers.Conv2D(32, (3, 3), activation=tf.nn.relu),
        keras.layers.MaxPooling2D(2, 2),
        keras.layers.Dropout(0.2),
        keras.layers.Flatten(),
        keras.layers.Dense(128, activation=tf.nn.relu),
        keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
```
主体为为卷积层、最大池化，并进行随即失活，激活函数均采用线性整流单元，最后两层为全连接层，最后结果通过softmax形式呈现

在优化器方面选择adam模型进行优化，来减小方差并加速梯度下降，且该问题为多分类问题，损失函数采parse_categorical_crossentropy
compel部分代码如下：
```python
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
```
最后进行训练(10次迭代)和测试，代码如下
```python
    model.fit(x_train, y_train, epochs=10)

    model.evaluate(x_test, y_test, verbose=2)
```
测试结果精度为0.9984

将模型作为h5文件导出，便于后续使用
####GUI
这里采用Pyqt5和qt designer来构建图形界面，该界面支持在窗体中用鼠标绘画，并通过捕获lable（即框中）的部分图片，使用之前训练的模型进行预测
效果图如下：
![](./Screen%20Shot%202022-09-07%20at%2018.58.07.png)
![](./Screen%20Shot%202022-09-07%20at%2018.58.27.png)
![](./Screen%20Shot%202022-09-07%20at%2018.58.38.png)

###整体逻辑
用户首先在界面中用鼠标写字（通过qpainter实现），在按下识别按钮时对屏幕中框体所在区域截图，并对图像进行处理，处理为（28，28，1）的灰度图，接着载入训练好的模型，进行预测，结果显示在另一个label中