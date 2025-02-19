import tensorflow as tf
import numpy as np
from copy import deepcopy

model = tf.keras.models.load_model("../lib/ml_model.keras")

total = 0
max_afternoons = 0

for i in range(15, 180):
    total += 2
    arr = [i] + [0] * 6
    all_times = [deepcopy(arr) for _ in range(8)]
    for i in range(4, 8):
        all_times[i][-1] = 1
    for i in range(4):
        all_times[i][-2] = 1
        all_times[i][1 + i] = 1
        all_times[4 + i][1 + i] = 1

    all_times = np.array(all_times)

    predictions = model.predict(all_times)

    if predictions[2] == max(predictions[:4]):
        max_afternoons += 1

    if predictions[6] == max(predictions[4:]):
        max_afternoons += 1

print("Percentage:", max_afternoons/total)
print("Total:", total)
print("Max afternoons:", max_afternoons)