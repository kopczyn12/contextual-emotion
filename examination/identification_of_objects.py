import cv2
import numpy as np
import pandas as pd

classes = {
    'cat': (0, 255, 0),
    'dog': (255, 0, 0),
    'duck': (0, 0, 255),
    'bunny': (255, 255, 0),
    'trash': (255, 0, 255),
    'tire': (0, 255, 255),
    'factory': (128, 0, 0),
    'car': (0, 128, 0),
    'human': (0, 0, 128),
    'deer': (128, 128, 0),
    'wolf': (128, 0, 128),
    'zombie': (0, 128, 128),
    'pig': (192, 0, 0),
    'head': (0, 192, 0),
    'guinea': (0, 0, 192),
    'fire': (192, 192, 0),
    'smoke': (0, 192, 192),
    'ruins': (128, 64, 0),
    'hanged_man': (0, 128, 64),
    'free_fall': (64, 128, 0),
    'pennywise': (128, 0, 64),
    'skull': (0, 64, 128),
    'barn': (255, 128, 0)
}

def check_class(image_path, x, y):
    """
    Checks the class of a pixel in an image.

    This function reads an image, retrieves the color of the pixel at a specified location,
    and checks the `classes` dictionary to see if the color corresponds to a known class.

    Args:
        image_path: The path of the image to check.
        x: The x-coordinate of the pixel to check.
        y: The y-coordinate of the pixel to check.

    Returns:
        The name of the class that corresponds to the color of the specified pixel, or
        'not defined' if the color does not correspond to a known class.
    """
    image = cv2.imread(image_path)
    size = image.size

    bgr_color = image[y, x]

    for class_name, class_color in classes.items():
        if np.array_equal(bgr_color, class_color):
            return class_name         
    return 'not defined'


df = pd.read_csv('/home/mkopcz/Desktop/contextual-emotion/examination/examination_merged/merged_file_smooth_kuba30@gmail.csv')


glupi_dict = {'surprise1.png': 0, 
'surprise2.png': 1, 
'surprise3.png': 2, 
'surpise4.png': 3, 
'surpise5.png': 4, 
'surprise6.png': 5, 
'surprise7.png': 6, 
'happy1.png': 7, 
'happy2.png': 8, 
'happy3.png': 9, 
'happy4.png': 10, 
'happy5.png': 11, 
'happy6.png': 12, 
'happy7.png': 13, 
'sad1.png': 14, 
'sad2.png': 15, 
'sad3.png': 16, 
'sad4.png': 17, 
'sad5.png': 18, 
'sad7.png': 19, 
'sad8.png': 20, 
'disgust1.png': 21, 
'disgust2.png': 22, 
'disgust3.png': 23, 
'disgust4.png': 24, 
'disgust5.png': 25, 
'disgust6.png': 26, 
'disgust7.png': 27, 
'angry1.png': 28, 
'angry2.png': 29, 
'angry3.png': 30, 
'angry4.png': 31, 
'angry5.png': 32, 
'angry6.png': 33, 
'angry7.png': 34}


numbers = df.iloc[:, 2].tolist()
x_logs = df.iloc[:, -2].tolist()
y_logs = df.iloc[:, -1].tolist()
#data = pd.concat([numbers, x_log, y_log], axis=1)

objects = []
counter = 0
for num in numbers:
    for key, value in glupi_dict.items():
        if value == num:
            image = key
            #try:
            x_log = int(x_logs[counter])
            y_log = int(y_logs[counter])

            if x_log >= 1920:
                x_log = 1919
            if y_log >= 1080:
                y_log = 1079
            detected_obj = check_class(f'/home/mkopcz/Desktop/contextual-emotion/segmentation/final_segmentation/mask/{key}', x_log, y_log)
            counter += 1
            objects.append(detected_obj)
            break


df['object'] = objects
df = df.drop('email', axis='columns')
df.rename(columns= {'Unnamed: 0': 'Index'}, inplace=True)
df.to_csv('/home/mkopcz/Desktop/contextual-emotion/examination/identification_of_objects/final_results_kuba30@gmail.com.csv', index=False)
