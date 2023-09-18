import os
from pathlib import Path
from PIL import Image

def convert_images_to_png(input_directory: str, output_directory: str) -> None:
    """
    Convert images from different formats to PNG.

    This function scans the input directory for images with supported extensions (.jpg, .jpeg, .png, .gif, .bmp)
    and converts them to PNG format, saving the converted images into the output directory. If the output directory
    does not exist, it gets created.

    :param input_directory: Path to the directory with images to be converted.
    :type input_directory: str
    :param output_directory: Path to the directory where converted images will be saved.
    :type output_directory: str
    :return: None

    """

    # Create output directory if it does not exist
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    # Iterate through all files in the input directory
    for filename in os.listdir(input_directory):
        # Check if the file has a supported image extension
        if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            # Load the image
            input_path = os.path.join(input_directory, filename)
            image = Image.open(input_path)

            # Convert the image to PNG and save it in the output directory
            output_filename = os.path.splitext(filename)[0] + '.png'
            output_path = os.path.join(output_directory, output_filename)
            image.save(output_path, 'PNG')

            print(f'Converted {input_path} to {output_path}')


# You can call the function like this:
convert_images_to_png('path_to_input', 'path_to_output')
