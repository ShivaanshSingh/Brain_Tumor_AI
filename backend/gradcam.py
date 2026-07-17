# import tensorflow as tf
# import numpy as np
# import cv2
# import os


# def generate_gradcam(model, img_array, predicted_index, save_path):

#     # Last Conv Layer
#     last_conv_layer = None

#     for layer in reversed(model.layers):
#         if isinstance(layer, tf.keras.layers.Conv2D):
#             last_conv_layer = layer.name
#             break

#     if last_conv_layer is None:
#         raise ValueError("No Conv2D layer found.")

#     # Grad Model
#     grad_model = tf.keras.models.Model(
#         [model.inputs],
#         [
#             model.get_layer(last_conv_layer).output,
#             model.output[0]
#         ]
#     )

#     with tf.GradientTape() as tape:

#         conv_outputs, predictions = grad_model(img_array)

#         loss = predictions[:, predicted_index]

#     grads = tape.gradient(loss, conv_outputs)

#     pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

#     conv_outputs = conv_outputs[0]

#     heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]

#     heatmap = tf.squeeze(heatmap)

#     heatmap = tf.maximum(heatmap, 0)

#     # heatmap /= tf.math.reduce_max(heatmap)
#     max_value=tf.math.reduce_max(heatmap)

#     if max_value !=0:
#         heatmap /=max_value

#     heatmap = heatmap.numpy()

#     heatmap = cv2.resize(heatmap, (150, 150))

#     heatmap = np.uint8(255 * heatmap)

#     heatmap = cv2.applyColorMap(
#         heatmap,
#         cv2.COLORMAP_JET
#     )

#     # Original Image
#     original = (img_array[0] * 255).astype(np.uint8)

#     original = cv2.cvtColor(
#         original,
#         cv2.COLOR_RGB2BGR
#     )

#     # Overlay
#     overlay = cv2.addWeighted(
#         original,
#         0.6,
#         heatmap,
#         0.4,
#         0
#     )

#     os.makedirs("heatmaps", exist_ok=True)

#     cv2.imwrite(save_path, overlay)

#     return save_path

import os
import cv2
import numpy as np
import tensorflow as tf


# Cache to avoid recreating the model on every request
CACHED_GRAD_MODEL = None

def generate_gradcam(model, img_array, predicted_index, save_path):
    global CACHED_GRAD_MODEL

    if CACHED_GRAD_MODEL is None:
        # Find last Conv2D layer
        last_conv_layer = None

        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer
                break

        if last_conv_layer is None:
            raise ValueError("No Conv2D layer found in model.")

        # Create model for Grad-CAM
        CACHED_GRAD_MODEL = tf.keras.Model(
            inputs=model.input,
            outputs=[last_conv_layer.output, model.output]
        )

    grad_model = CACHED_GRAD_MODEL

    with tf.GradientTape() as tape:

        conv_outputs, predictions = grad_model(img_array)
        print("Prediction Shape :", predictions.shape)

        class_channel = predictions[:, predicted_index]

    # Gradients
    grads = tape.gradient(class_channel, conv_outputs)

    # Mean gradients
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]

    # Weight feature maps
    heatmap = tf.reduce_sum(
        conv_outputs * pooled_grads,
        axis=-1
    )

    heatmap = tf.maximum(heatmap, 0)

    heatmap = heatmap / (tf.reduce_max(heatmap) + 1e-8)

    heatmap = heatmap.numpy()

    # Resize
    heatmap = cv2.resize(
        heatmap,
        (150, 150)
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    # Original Image
    original = (img_array[0] * 255).astype(np.uint8)

    original = cv2.cvtColor(
        original,
        cv2.COLOR_RGB2BGR
    )

    # Overlay
    overlay = cv2.addWeighted(
        original,
        0.6,
        heatmap,
        0.4,
        0
    )

    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    cv2.imwrite(save_path, overlay)

    return save_path