import tensorflow as tf
from tensorflow import keras
from extra_keras_datasets import emnist

(x_train, y_train), (x_test, y_test) = emnist.load_data(type='balanced')
x_train, x_test = x_train / 255.0, x_test / 255.0

model = keras.models.Sequential([
    keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu, input_shape=(28, 28, 1)),
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Conv2D(64, (3, 3), activation=tf.nn.relu),
    keras.layers.MaxPooling2D(2, 2),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(47, activation=tf.nn.softmax)
])

model.summary()

model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
)

model.fit(x_train, y_train, epochs=5)

model.evaluate(x_test,  y_test, verbose=2)

save_model_path = "./"
tf.keras.experimental.export_saved_model(model, save_model_path)





