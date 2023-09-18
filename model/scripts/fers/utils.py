""" Helper functions used across more than one script"""
import numpy as np


def string_to_numpy_array(pixels_str: str, shape: tuple[int, int] = (48, 48)) -> np.ndarray:
    """ Converts an image represented by a str with grayscale pixel values to a numpy array """
    pixel_list: list[int] = list(map(int, pixels_str.split(' ')))
    pixel_array: np.ndarray = np.array(pixel_list).reshape(shape)

    return pixel_array.astype('int32')
