
# # Brain Tumor CNN Model

# import tensorflow as tf
# from tensorflow.keras import layers, models

# # Dataset path
# train_dir = "dataset/Training"
# test_dir = "dataset/Testing"

# # Image size
# IMG_SIZE = 150
# BATCH_SIZE = 32

# # Load Training Data
# train_data = tf.keras.preprocessing.image_dataset_from_directory(
#     train_dir,
#     image_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     shuffle=True
# )

# # Load Testing Data
# test_data = tf.keras.preprocessing.image_dataset_from_directory(
#     test_dir,
#     image_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     shuffle=False
# )

# # Class Names
# class_names = train_data.class_names
# print("Classes:", class_names)

# # Normalize Images
# normalization = layers.Rescaling(1.0 / 255)

# train_data = train_data.map(lambda x, y: (normalization(x), y))
# test_data = test_data.map(lambda x, y: (normalization(x), y))

# # Improve Performance
# AUTOTUNE = tf.data.AUTOTUNE

# train_data = train_data.prefetch(buffer_size=AUTOTUNE)
# test_data = test_data.prefetch(buffer_size=AUTOTUNE)

# # CNN Model
# model = models.Sequential([
#     layers.Input(shape=(150, 150, 3)),

#     layers.Conv2D(32, (3, 3), activation="relu"),
#     layers.MaxPooling2D(),

#     layers.Conv2D(64, (3, 3), activation="relu"),
#     layers.MaxPooling2D(),

#     layers.Conv2D(128, (3, 3), activation="relu"),
#     layers.MaxPooling2D(),

#     layers.Flatten(),

#     layers.Dense(128, activation="relu"),

#     layers.Dense(len(class_names), activation="softmax")
# ])

# # Compile
# model.compile(
#     optimizer="adam",
#     loss="sparse_categorical_crossentropy",
#     metrics=["accuracy"]
# )

# # Train
# model.fit(
#     train_data,
#     validation_data=test_data,
#     epochs=10
# )

# # Save Model
# model.save("model/brain_tumor_model.keras")

# print("Model training complete!")


import tensorflow as tf
from tensorflow.keras import layers
import os

# Dataset Paths
train_dir = "dataset/Training"
test_dir = "dataset/Testing"

# Parameters
IMG_SIZE = 150
BATCH_SIZE = 32
EPOCHS = 10

# Load Training Dataset
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=True
)

# Load Testing Dataset
test_data = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

# Class Names
class_names = train_data.class_names
print("Classes:", class_names)

# Normalize Images
normalization_layer = layers.Rescaling(1.0 / 255)

train_data = train_data.map(
    lambda x, y: (normalization_layer(x), y)
)

test_data = test_data.map(
    lambda x, y: (normalization_layer(x), y)
)

# Performance
AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(AUTOTUNE)
test_data = test_data.prefetch(AUTOTUNE)

# -----------------------------
# Functional CNN Model
# -----------------------------

inputs = tf.keras.Input(shape=(150, 150, 3), name="input_layer")

x = layers.Conv2D(
    32,
    (3, 3),
    activation="relu",
    name="conv1"
)(inputs)

x = layers.MaxPooling2D(name="pool1")(x)

x = layers.Conv2D(
    64,
    (3, 3),
    activation="relu",
    name="conv2"
)(x)

x = layers.MaxPooling2D(name="pool2")(x)

x = layers.Conv2D(
    128,
    (3, 3),
    activation="relu",
    name="last_conv"
)(x)

x = layers.MaxPooling2D(name="pool3")(x)

x = layers.Flatten()(x)

x = layers.Dense(
    128,
    activation="relu"
)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax",
    name="predictions"
)(x)

model = tf.keras.Model(
    inputs=inputs,
    outputs=outputs,
    name="BrainTumorCNN"
)

# Compile
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# Summary
model.summary()

# Train
history = model.fit(
    train_data,
    validation_data=test_data,
    epochs=EPOCHS
)

# Evaluate
loss, accuracy = model.evaluate(test_data)

print(f"\nTest Accuracy : {accuracy*100:.2f}%")

# Save Model
os.makedirs("model", exist_ok=True)

model.save("model/brain_tumor_model.keras")

print("\nModel Saved Successfully.")