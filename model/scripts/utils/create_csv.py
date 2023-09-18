from PIL import Image
import numpy as np
import csv
import os

label = {
    "angry": 0,
    "disgust": 1,
    "happy": 2,
    "sad": 3,
    "surprise": 4
}

dataset_path_test = r"C:\Users\patry\OneDrive\Pulpit\dataset_split\test\\"
dataset_path_train = r"C:\Users\patry\OneDrive\Pulpit\dataset_split\train\\"

# zapisz ciąg pixeli do pliku CSV
with open(r'C:\Users\patry\OneDrive\Pulpit\dataset_split\nowe_dane.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['emotion', "pixels", 'Usage'])

    for emotion_folder in os.listdir(dataset_path_train):
        path = dataset_path_train + emotion_folder + "/"
        for image in os.listdir(path):
            img = Image.open(path + image).resize((48, 48)).convert('L')
            pixels = ' '.join(map(str, np.ravel(np.array(img))))
            writer.writerow([label[emotion_folder], pixels, "Training"])

    for emotion_folder in os.listdir(dataset_path_test):
        path = dataset_path_test + emotion_folder + "/"
        for image in os.listdir(path):
            img = Image.open(path + image).resize((48, 48)).convert('L')
            pixels = ' '.join(map(str, np.ravel(np.array(img))))
            writer.writerow([label[emotion_folder], pixels, "PublicTest"])