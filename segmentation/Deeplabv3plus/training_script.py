import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import cv2
import numpy as np
from glob import glob
from scipy.io import loadmat
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from keras import layers



IMAGE_SIZE = 256
BATCH_SIZE = 4
NUM_CLASSES = 22
NUM_TRAIN_IMAGES = 170
NUM_VAL_IMAGES = 20
    
image_extensions = ('*.png')

def get_image_paths(folder):
    """
    Get all image paths in a folder

    Args:
        folder: The folder to get image paths from

    Returns:
        A list of image paths
    
    
    """
    return [img_path for extension in image_extensions for img_path in glob(os.path.join(folder, extension)) if os.path.isfile(img_path)]


train_images = sorted(get_image_paths(''))[:NUM_TRAIN_IMAGES]   #Paths to images and masks
train_masks = sorted(get_image_paths(''))[:NUM_TRAIN_IMAGES]
val_images = sorted(get_image_paths(""))[
    NUM_TRAIN_IMAGES : NUM_VAL_IMAGES + NUM_TRAIN_IMAGES
]
val_masks = sorted(get_image_paths(''))[
    NUM_TRAIN_IMAGES : NUM_VAL_IMAGES + NUM_TRAIN_IMAGES
]



def read_image(image_path, mask=False):
    """
    Read an image from path

    Args:
        image_path: The path to the image 
        mask: Wheather the image is a mask

    Retuns:
        Image
    
    
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


def load_data(image_list, mask_list):
    """
    Load data from image and mask lists

    Args:
        image_list: List of images
        mask_list: List of masks

    Returns:
        Read image and mask
    """
    image = read_image(image_list)
    mask = read_image(mask_list, mask=True)
    return image, mask


def data_generator(image_list, mask_list):
    """
    Generates TF dataset from image and mask lists

    Args:
        image_list: The list of images
        mask_list: The list of masks

    Returns:
        A TF dataset
    """
    dataset = tf.data.Dataset.from_tensor_slices((image_list, mask_list))
    dataset = dataset.map(load_data, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(BATCH_SIZE, drop_remainder=True)
    return dataset


train_dataset = data_generator(train_images, train_masks)
val_dataset = data_generator(val_images, val_masks)

def convolution_block(
    block_input,
    num_filters=256,
    kernel_size=3,
    dilation_rate=1,
    padding="same",
    use_bias=False,
):
    """
    Define a convolution block.

    Args:
        block_input: The input to the block.
        num_filters: The number of filters.
        kernel_size: The kernel size.
        dilation_rate: The dilation rate.
        padding: The padding type.
        use_bias: Whether to use bias.

    Returns:
        The output of the convolution block.
    """
    x = layers.Conv2D(
        num_filters,
        kernel_size=kernel_size,
        dilation_rate=dilation_rate,
        padding="same",
        use_bias=use_bias,
        kernel_initializer=keras.initializers.HeNormal(),
    )(block_input)
    #x = layers.Flatten()(x)    ##
    x = layers.BatchNormalization()(x)
   # x = layers.Reshape((1,1,-1))(x)  ##
    return tf.nn.relu(x)


def DilatedSpatialPyramidPooling(dspp_input):
    """
    Define a dilated spatial pyramid pooling layer.

    Args:
        dspp_input: The input to the layer.

    Returns:
        The output of the dilated spatial pyramid pooling layer.
    """

    dims = dspp_input.shape
    x = layers.AveragePooling2D(pool_size=(dims[-3], dims[-2]))(dspp_input)
    x = convolution_block(x, kernel_size=1, use_bias=True)
    out_pool = layers.UpSampling2D(
        size=(dims[-3] // x.shape[1], dims[-2] // x.shape[2]), interpolation="bilinear",
    )(x)

    out_1 = convolution_block(dspp_input, kernel_size=1, dilation_rate=1)
    out_6 = convolution_block(dspp_input, kernel_size=3, dilation_rate=6)
    out_12 = convolution_block(dspp_input, kernel_size=3, dilation_rate=12)
    out_18 = convolution_block(dspp_input, kernel_size=3, dilation_rate=18)

    x = layers.Concatenate(axis=-1)([out_pool, out_1, out_6, out_12, out_18])
    output = convolution_block(x, kernel_size=1)
    return output

def DeeplabV3Plus(image_size, num_classes):
    """
    Define the DeepLabV3+ model.

    Args:
        image_size: The size of the input images.
        num_classes: The number of classes.

    Returns:
        The DeepLabV3+ model.
    """
    model_input = keras.Input(shape=(image_size, image_size, 3))
    resnet50 = keras.applications.ResNet50(
        weights="imagenet", include_top=False, input_tensor=model_input
    )
    x = resnet50.get_layer("conv4_block6_2_relu").output
    x = DilatedSpatialPyramidPooling(x)

    input_a = layers.UpSampling2D(
        size=(image_size // 4 // x.shape[1], image_size // 4 // x.shape[2]),
        interpolation="bilinear",
    )(x)
    input_b = resnet50.get_layer("conv2_block3_2_relu").output
    input_b = convolution_block(input_b, num_filters=48, kernel_size=1)

    x = layers.Concatenate(axis=-1)([input_a, input_b])
    x = convolution_block(x)
    x = convolution_block(x)
    x = layers.UpSampling2D(
        size=(image_size // x.shape[1], image_size // x.shape[2]),
        interpolation="bilinear",
    )(x)
    model_output = layers.Conv2D(num_classes, kernel_size=(1, 1), padding="same")(x)
    return keras.Model(inputs=model_input, outputs=model_output)


model = DeeplabV3Plus(image_size=IMAGE_SIZE, num_classes=NUM_CLASSES)
model.summary()

loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.001),
    loss=loss,
    metrics=["accuracy"],
)

history = model.fit(train_dataset, validation_data=val_dataset, epochs=70)

model.save("")   #path to model



plt.plot(history.history["loss"])
plt.title("Training Loss")
plt.ylabel("loss")
plt.xlabel("epoch")
plt.show()

plt.plot(history.history["accuracy"])
plt.title("Training Accuracy")
plt.ylabel("accuracy")
plt.xlabel("epoch")
plt.show()

plt.plot(history.history["val_loss"])
plt.title("Validation Loss")
plt.ylabel("val_loss")
plt.xlabel("epoch")
plt.show()

plt.plot(history.history["val_accuracy"])
plt.title("Validation Accuracy")
plt.ylabel("val_accuracy")
plt.xlabel("epoch")
plt.show()