
# import os
# import cv2
# import numpy as np


# def segment_tumor(image_path, save_path):

#     image = cv2.imread(image_path)

#     if image is None:
#         raise ValueError("Image not found.")

#     original = image.copy()

#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     blur = cv2.GaussianBlur(gray, (5, 5), 0)

#     # _,
#     thresh = cv2.adaptiveThreshold(
#         blur,
#         255,
#         cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY,
#         11,
#         2
#     )

#     kernel = cv2.getStructuringElement(
#         cv2.MORPH_ELLIPSE,
#         (5,5)
#     )

#     thresh = cv2.morphologyEx(
#         thresh,
#         cv2.MORPH_CLOSE,
#         kernel,
#         iterations=3
#     )

#     thresh=cv2.erode(
#         thresh,
#         kernel,
#         iterations=1
#     )
#     thresh=cv2.dilate(
#         thresh,
#         kernel,
#         iterations=2
#     )

#     contours, _ = cv2.findContours(
#         thresh,
#         cv2.RETR_EXTERNAL,
#         cv2.CHAIN_APPROX_SIMPLE
#     )

#     segmented = original.copy()

#     width = 0
#     height = 0
#     area = 0

#     center_x = 0
#     center_y = 0
#     region = "Unknown"

#     if len(contours) > 0:

#         contour = max(contours, key=cv2.contourArea)

#         area = float(cv2.contourArea(contour))

#         x, y, w, h = cv2.boundingRect(contour)

#         width = int(w)
#         height = int(h)

#         center_x = int(x + w / 2)
#         center_y = int(y + h / 2)

#         # Image dimensions
#         img_height, img_width = image.shape[:2]

#         # Horizontal position
#         if center_x < img_width / 2:
#             horizontal = "Left"
#         else:
#             horizontal = "Right"

#         # Vertical position
#         if center_y < img_height / 2:
#             vertical = "Top"
#         else:
#             vertical = "Bottom"

#         region = f"{vertical} {horizontal}"

#         # Draw contour
#         cv2.drawContours(
#             segmented,
#             [contour],
#             -1,
#             (0, 255, 0),
#             2
#         )

#         # Draw bounding box
#         cv2.rectangle(
#             segmented,
#             (x, y),
#             (x + w, y + h),
#             (0, 0, 255),
#             2
#         )

#     os.makedirs("segmentations", exist_ok=True)

#     cv2.imwrite(save_path, segmented)

#     return {
#         "segmentationPath": save_path,
#         "tumorSize": {
#             "width": width,
#             "height": height,
#             "area": round(area, 2)
#         },
#         "location": {
#             "x": center_x,
#             "y": center_y,
#             "region": region
#         }
#     }
import os
import cv2
import numpy as np


def segment_tumor(image_path, save_path):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Image not found.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise remove
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Bright tumor regions
    thresh = cv2.threshold(
        blur,
        180,
        255,
        cv2.THRESH_BINARY
    )[1]

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (7, 7)
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=2
    )

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_CLOSE,
        kernel,
        iterations=3
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    segmented = image.copy()

    width = 0
    height = 0
    area = 0
    center_x = 0
    center_y = 0
    region = "Unknown"

    best_contour = None
    best_area = 0

    img_h, img_w = gray.shape

    for cnt in contours:

        a = cv2.contourArea(cnt)

        if a < 300:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Ignore image border
        if x < 15 or y < 15:
            continue

        if x + w > img_w - 15:
            continue

        if y + h > img_h - 15:
            continue

        if a > best_area:
            best_area = a
            best_contour = cnt

    if best_contour is not None:

        area = float(cv2.contourArea(best_contour))

        x, y, w, h = cv2.boundingRect(best_contour)

        width = w
        height = h

        center_x = x + w // 2
        center_y = y + h // 2

        horizontal = "Left" if center_x < img_w/2 else "Right"
        vertical = "Top" if center_y < img_h/2 else "Bottom"

        region = f"{vertical} {horizontal}"

        # Filled tumor
        overlay = segmented.copy()

        cv2.drawContours(
            overlay,
            [best_contour],
            -1,
            (0,255,0),
            -1
        )

        segmented = cv2.addWeighted(
            overlay,
            0.35,
            segmented,
            0.65,
            0
        )

        # Outline
        cv2.drawContours(
            segmented,
            [best_contour],
            -1,
            (0,255,0),
            3
        )

        # Bounding box
        cv2.rectangle(
            segmented,
            (x,y),
            (x+w,y+h),
            (0,0,255),
            2
        )

        # Center point
        cv2.circle(
            segmented,
            (center_x,center_y),
            5,
            (255,0,0),
            -1
        )

    os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)

    cv2.imwrite(save_path, segmented)

    return {
        "segmentationPath": save_path,
        "tumorSize": {
            "width": width,
            "height": height,
            "area": round(area,2)
        },
        "location": {
            "x": center_x,
            "y": center_y,
            "region": region
        }
    }