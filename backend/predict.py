
# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# from gradcam import generate_gradcam
# from segmentation import segment_tumor

# # Load Trained Model
# model = tf.keras.models.load_model("model/brain_tumor_model.keras")
# dummy = np.zeros((1, 150, 150, 3), dtype=np.float32)
# _ = model(dummy)
# # print(model.summary())
# # print(model.inputs)
# # print(model.outputs)
# # Same order as training dataset
# class_names = [
#     "glioma",
#     "meningioma",
#     "notumor",
#     "pituitary"
# ]


# # Predict Function
# def predict_tumor(image_path):

#     try:
#         # Load Image
#         img = image.load_img(
#             image_path,
#             target_size=(150, 150)
#         )

#         # Convert Image to Array
#         img_array = image.img_to_array(img)

#         # Normalize
#         img_array = img_array / 255.0

#         # Add Batch Dimension
#         img_array = np.expand_dims(img_array, axis=0)

#         # Prediction
#         prediction = model.predict(img_array, verbose=0)

#         # Highest Probability Index
#         predicted_index = np.argmax(prediction)

#         # Predicted Class
#         predicted_class = class_names[predicted_index]

#         # Confidence
#         confidence = round(
#             float(prediction[0][predicted_index] * 100),
#             2
#         )

#         # # Generate Heatmap
#         os.makedirs("heatmaps", exist_ok=True)

#         heatmap_filename = os.path.basename(image_path)

#         heatmap_path = os.path.join(
#             "heatmaps",
#             heatmap_filename
#         )

#         generate_gradcam(
#             model,
#             img_array,
#             predicted_index,
#             heatmap_path
#         )

#     # segmentation
#     os.makedirs("segmentations", exist_ok=True)
#     segmentation_filename = os.path.basename(image_path)
#     segmentation_path = os.path.join(
#         "segmentations",
#         segmentation_filename
#     )

#     segmentation_result = segment_tumor(
#         image_path,
#         segmentation_path
#     )

#         # User Friendly Name
#         if predicted_class == "notumor":
#             tumor_type = "No Tumor"
#             tumor_detected = False
#         else:
#             tumor_type = predicted_class.capitalize()
#             tumor_detected = True

#         return {
#             "success": True,

#             "tumorDetected": tumor_detected,

#             "tumorType": tumor_type,

#             "confidence": confidence,

#             "heatmapPath": heatmap_path,

#             "segmentationPath": segmentation_result["segmentationPath"],
#             "tumorSize": segmentation_result["tumorSize"],
#             "location": segmentation_result["location"],


#             "probabilities": {
#                 "glioma": round(float(prediction[0][0] * 100), 2),
#                 "meningioma": round(float(prediction[0][1] * 100), 2),
#                 "noTumor": round(float(prediction[0][2] * 100), 2),
#                 "pituitary": round(float(prediction[0][3] * 100), 2),
#             }
#         }

#     except Exception as e:

#         return {
#             "success": False,
#             "message": str(e)
#         }
import os
# Suppress TensorFlow warnings and oneDNN custom operations logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)
import numpy as np
import tensorflow as tf
# pyrefly: ignore [missing-import]
from tensorflow.keras.preprocessing import image

from gradcam import generate_gradcam
from segmentation import segment_tumor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load Trained Model
model_path = os.path.join(BASE_DIR, "model", "brain_tumor_model.keras")
model = tf.keras.models.load_model(model_path)

dummy = np.zeros((1, 150, 150, 3), dtype=np.float32)
_ = model(dummy)

# Same order as training dataset
class_names = [
    "glioma",
    "meningioma",
    "notumor",
    "pituitary"
]


def predict_tumor(image_path):

    try:

        # Load Image
        img = image.load_img(
            image_path,
            target_size=(150, 150)
        )

        # Convert Image to Array
        img_array = image.img_to_array(img)

        # Normalize
        img_array = img_array / 255.0

        # Add Batch Dimension
        img_array = np.expand_dims(img_array, axis=0)

        # Prediction
        prediction_tensor = model(
            img_array,
            training=False
        )
        prediction = prediction_tensor.numpy()

        # Highest Probability Index
        predicted_index = np.argmax(prediction)

        # Predicted Class
        predicted_class = class_names[predicted_index]

        # Confidence
        confidence = round(
            float(prediction[0][predicted_index] * 100),
            2
        )

       
        # Generate Grad-CAM Heatmap
        

        heatmap_dir = os.path.join(BASE_DIR, "heatmaps")
        os.makedirs(heatmap_dir, exist_ok=True)

        heatmap_filename = os.path.basename(image_path)

        heatmap_path = os.path.join(
            heatmap_dir,
            heatmap_filename
        )

        generate_gradcam(
            model,
            img_array,
            predicted_index,
            heatmap_path
        )

       
        # Generate Segmentation
        

        segmentation_dir = os.path.join(BASE_DIR, "segmentations")
        os.makedirs(segmentation_dir, exist_ok=True)

        segmentation_filename = os.path.basename(image_path)

        segmentation_path = os.path.join(
            segmentation_dir,
            segmentation_filename
        )

        segmentation_result = segment_tumor(
            image_path,
            segmentation_path
        )

        # User Friendly Result
       

        if predicted_class == "notumor":
            tumor_type = "No Tumor"
            tumor_detected = False
        else:
            tumor_type = predicted_class.capitalize()
            tumor_detected = True


        # Calculate Severity
        area = segmentation_result["tumorSize"]["area"]
        if not tumor_detected:
            severity="None"
        elif area==0:
            severity="Needs Review"
        elif area < 5000:
            severity = "Low"
        elif area < 20000:
            severity = "Medium"
        else:
            severity= "High"

       
        
        # Return Response
        
        return {

            "success": True,

            "tumorDetected": tumor_detected,

            "tumorType": tumor_type,

            "confidence": confidence,

            "heatmapPath": heatmap_path,

            "segmentationPath": segmentation_result["segmentationPath"],

            "tumorSize": segmentation_result["tumorSize"],

            "location": segmentation_result["location"],
            "severity": severity,

            "probabilities": {
                "glioma": round(float(prediction[0][0] * 100), 2),
                "meningioma": round(float(prediction[0][1] * 100), 2),
                "noTumor": round(float(prediction[0][2] * 100), 2),
                "pituitary": round(float(prediction[0][3] * 100), 2),
            }

        }

    except Exception as e:

        return {
            "success": False,
            "message": str(e)
        }