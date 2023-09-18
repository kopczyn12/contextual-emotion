"""
Script containing a function for aligning faces in a dataset in form of a numpy array of grayscale images
Returns a numpy array of the same shape and size as original, but with a face aligned using FAN
"""
import numpy as np
import cv2
import face_alignment

# initialize the face_alignment module
fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False)


def align_face(image):
    """
    Function aligning the face to be centered in the photo
    :param image: Face to be centered
    :return: Face centered using FAN model
    """
    # FAN was trained on RGB images, we need to triple the grayscale values so that the image is
    # of shape (width, height, 3)
    if (len(image.shape) >= 3):
        image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Detect landmarks in the image using FAN
    landmarks = fa.get_landmarks(image_color)

    if landmarks is None:
        return image

    landmarks = landmarks[0]

    center_of_mass = landmarks.mean(axis=0)

    # landmarks for eyes are obtained from the face_alignment module documentation
    # Calculate the angle to rotate, to align the eyes horizontally
    eye_left = landmarks[36]
    eye_right = landmarks[45]
    dx = eye_right[0] - eye_left[0]
    dy = eye_right[1] - eye_left[1]
    angle = np.degrees(np.arctan2(dy, dx))

    rotation_matrix = cv2.getRotationMatrix2D(tuple(center_of_mass), angle, 1)
    aligned_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]), flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_REFLECT)

    return aligned_image
