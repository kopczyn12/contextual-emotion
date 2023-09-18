""" Script for creating a face-aligned csv with only 5 emotions we are taking into consideration """
import os
import pandas as pd
import cv2
from fan_face_alignment import *


# Put dataset from https://www.kaggle.com/datasets/shawon10/ckplus into the directory below and
# rename the folder to 'ckplus'
csv_path: str = os.path.join(os.getcwd(), os.pardir, "dataset_ckplus")
csv_name = "ckextended_aligned.csv"
images_base_path: str = os.path.join(csv_path, "ckplus")
dataset_emotions = ["anger", "disgust", "happy", "sadness", "surprise"]
emotion_labels = []
pixel_values = []

# If ckextended_aligned.csv exists, omit this part
if not os.path.exists(os.path.join(csv_path, csv_name)):
    for i, emotion in enumerate(dataset_emotions):
        emotion_directory_path = os.path.join(images_base_path, emotion)

        if os.path.isdir(emotion_directory_path):
            for filename in os.listdir(emotion_directory_path):
                if filename.endswith((".png")):
                    image_path = os.path.join(emotion_directory_path, filename)

                    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    # Align faces using FAN
                    img = align_face(img)

                    # To be consistent with other ckplus representation
                    pixel_string = ' '.join(map(str, img.flatten()))

                    emotion_labels.append(i)
                    pixel_values.append(pixel_string)

    ckplus_df = pd.DataFrame({
        'emotion': emotion_labels,
        'pixels': pixel_values
    })

    ckplus_df.to_csv(os.path.join(csv_path, csv_name), index=False)
