import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("../lib/ml_model.keras")

test = [[80, 0, 1, 0, 0, 1, 0]]

test = np.array(test)

print(model.predict(test))