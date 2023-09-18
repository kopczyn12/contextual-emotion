import os
import cv2
import numpy as np
from glob import glob
from scipy.io import loadmat
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from keras import layers

model = keras.models.load_model("models/fifth.h5")  # model path

IMAGE_SIZE = 256

colormap = loadmat(
    "colormap_3.mat"
)["colormap"]
colormap = colormap * 100
colormap = colormap.astype(np.uint8)


def infer(model, image_tensor):
    """
    Run inference on an image tensor using a model.

    Args:
        model: The model to use for inference.
        image_tensor: The image tensor to infer on.

    Returns:
        The model's predictions.
    """
    predictions = model.predict(np.expand_dims((image_tensor), axis=0))
    predictions = np.squeeze(predictions)
    predictions = np.argmax(predictions, axis=2)
    return predictions


def decode_segmentation_masks(mask, colormap, n_classes):
    """
    Decode segmentation masks into RGB images.

    Args:
        mask: The mask to decode.
        colormap: The colormap to use for decoding.
        n_classes: The number of classes.

    Returns:
        The decoded RGB image.
    """
    r = np.zeros_like(mask).astype(np.uint8)
    g = np.zeros_like(mask).astype(np.uint8)
    b = np.zeros_like(mask).astype(np.uint8)
    for l in range(0, n_classes):
        idx = mask == l
        r[idx] = colormap[l, 0]
        g[idx] = colormap[l, 1]
        b[idx] = colormap[l, 2]
    rgb = np.stack([r, g, b], axis=2)
    return rgb


def get_overlay(image, colored_mask):
    """
    Apply an overlay on top of an image.

    Args:
        image: The base image.
        colored_mask: The overlay to apply.

    Returns:
        The image with the overlay applied.
    """
    image = tf.keras.utils.array_to_img(image)
    image = np.array(image).astype(np.uint8)
    overlay = cv2.addWeighted(image, 0.35, colored_mask, 0.65, 0)
    return overlay


def plot_samples_matplotlib(display_list, figsize=(5, 3)):
    """
    Plot samples using Matplotlib.

    Args:
        display_list: The list of samples to plot.
        figsize: The size of the figure.

    Returns:
        None
    """
    _, axes = plt.subplots(nrows=1, ncols=len(display_list), figsize=figsize)
    for i in range(len(display_list)):
        if display_list[i].shape[-1] == 3:
            axes[i].imshow(tf.keras.utils.array_to_img(display_list[i]))
        else:
            axes[i].imshow(display_list[i])
    plt.show()


def plot_predictions(images_list, colormap, model):
    """
    Plot predictions for a list of images.

    Args:
        images_list: The list of images to predict on.
        colormap: The colormap to use for decoding masks.
        model: The model to use for predictions.

    Returns:
        None
    """
    for image_file in images_list:
        image_tensor = read_image(image_file)
        prediction_mask = infer(image_tensor=image_tensor, model=model)
        prediction_colormap = decode_segmentation_masks(prediction_mask, colormap, 20)
        overlay = get_overlay(image_tensor, prediction_colormap)
        plot_samples_matplotlib(
            [image_tensor, overlay, prediction_colormap], figsize=(18, 14)
        )


def read_image(image_path, mask=False):
    """
    Read an image from a file.

    Args:
        image_path: The path to the image.
        mask: Whether the image is a mask.

    Returns:
        The image.
    """
    image = tf.io.read_file(image_path)
    if mask:
        image = tf.image.decode_png(image, channels=1)
        image.set_shape([None, None, 1])
        image = tf.image.resize(images=image, size=[IMAGE_SIZE, IMAGE_SIZE])
    else:
        image = tf.image.decode_png(image, channels=3)
        image.set_shape([None, None, 3])
        image = tf.image.resize(images=image, size=[IMAGE_SIZE, IMAGE_SIZE])
        image = tf.keras.applications.resnet50.preprocess_input(image)
    return image


dataset_dir = ""  # directory with images to segment
image_files = []

for filename in os.listdir(dataset_dir):
    file_path = os.path.join(dataset_dir, filename)
    image_files.append(file_path)
    

plot_predictions(images_list=image_files, colormap=colormap, model=model)
