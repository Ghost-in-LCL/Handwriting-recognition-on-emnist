##手写字识别
刘佩汉

————————
由于本机开发环境为mac os不能打包为exe，所以没能将项目打包

项目中model为基于Emnist数据集的47类手写字识别的模型，但效果不理想，在测试中发现偏差过大，可能需要建立更深的神经网络或是更多的迭代次数，因此主体为基于Mnist手写数字识别即test

在bin中的为两神经网络源码，和基于qt designer构建的ui源码
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