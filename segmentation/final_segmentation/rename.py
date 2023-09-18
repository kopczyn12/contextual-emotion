import os
import shutil

def rename_mask_files(masks_path):
    """
    Renames all mask files in a directory by removing the '_mask' substring 
    from their filenames.

    Args:
        masks_path (str): The path to the directory containing the mask files.
    """
    # Loop through all files in the masks folder
    for filename in os.listdir(masks_path):
        # Check if the filename contains the substring '_mask'
        if '_mask' in filename:
            # Remove the substring '_mask' from the filename
            new_filename = filename.replace('_mask', '')
            # Construct the full path to the old and new files
            old_path = os.path.join(masks_path, filename)
            new_path = os.path.join(masks_path, new_filename)
            # Rename the file by moving it to a new file with the desired name
            shutil.move(old_path, new_path)

# Set the path to your masks folder
masks_path = ''
rename_mask_files(masks_path)
