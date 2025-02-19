import tensorflow as tf
import pandas as pd
import numpy as np

column_names = ["Time", "Type", "Duration", "Satisfaction"]

raw_dataset = pd.read_csv("../data/student_dataset_sat.csv", names=column_names)

dataset = raw_dataset.copy()

dataset["Time"] = dataset["Time"].map({"Morning": 1, "Afternoon": 2, "Evening": 3, "Night": 4})
dataset["Type"] = dataset["Type"].map({"Exercise": 1, "Relaxation": 2})

dataset = pd.get_dummies(dataset, columns=["Time", "Type"])
dataset = dataset.astype(int)

train_features = dataset.copy()
train_labels = train_features.pop("Satisfaction")

normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_features))

linear_model = tf.keras.Sequential([normalizer, tf.keras.layers.Dense(1)])

linear_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
                     loss="mean_absolute_error")

linear_model.fit(
    train_features,
    train_labels,
    epochs=5,
    validation_split=0.2,
)

linear_model.save("ml_model.keras")