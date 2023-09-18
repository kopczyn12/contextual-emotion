import cv2
import os

def resize_images_and_masks(img_dir, mask_dir, res_img_dir, res_mask_dir, new_size):
    """
    Resizes images and corresponding masks and saves them in new directories.

    Args:
        img_dir (str): Directory containing the original images.
        mask_dir (str): Directory containing the original mask images.
        res_img_dir (str): Directory to save the resized images.
        res_mask_dir (str): Directory to save the resized mask images.
        new_size (tuple): Desired size for the images and masks after resizing.
    """
    # Create directories if they do not exist
    if not os.path.exists(res_img_dir):
        os.makedirs(res_img_dir)
    if not os.path.exists(res_mask_dir):  # For the resized masks
        os.makedirs(res_mask_dir)

    # Loop through all files in the image directory
    for filename in os.listdir(img_dir):
        # Resize the image
        img = cv2.imread(os.path.join(img_dir, filename))
        img_resized = cv2.resize(img, new_size, interpolation=cv2.INTER_LINEAR)
        cv2.imwrite(os.path.join(res_img_dir, filename), img_resized)

        # Resize the corresponding mask
        mask = cv2.imread(os.path.join(mask_dir, filename))
        mask_resized = cv2.resize(mask, new_size, interpolation=cv2.INTER_NEAREST)
        cv2.imwrite(os.path.join(res_mask_dir, filename), mask_resized)

img_dir = ""
mask_dir = ""  
res_img_dir = ""
res_mask_dir = ""  
new_size = (1920, 1080)

resize_images_and_masks(img_dir, mask_dir, res_img_dir, res_mask_dir, new_size)
