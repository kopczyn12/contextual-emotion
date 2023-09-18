import os
import json
import cv2
import numpy as np

classes = {'cat': (0, 255, 0),
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
          # 'guinea': (0, 0, 192),
           'fire': (192, 192, 0),
         #  'watermelon': (192, 0, 192),
           'smoke': (0, 192, 192),
           'ruins': (128, 64, 0),
           'hanged_man': (0, 128, 64),
           'free_fall': (64, 128, 0),
           'pennywise': (128, 0, 64),
           'skull': (0, 64, 128),
           'barn': (255, 128, 0)
           }


def create_masks_overlays(data, img_dir, msk_dir, overlay_dir):
    """
    Process data to create mask images and overlays, then save them in provided directories.

    Args:
        data (dict): JSON parsed data with annotation details.
        img_dir (str): Directory containing the original images.
        msk_dir (str): Directory to save the mask images.
        overlay_dir (str): Directory to save the overlay images.
    """
    data = data["_via_img_metadata"]
    
    for key, value in data.items():
        used_classes = {} # keep track of used classes
        filename = value["filename"]
        img_path = f"{img_dir}/{filename}"
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        h, w,_  = img.shape
        mask = np.zeros((h, w, 3), dtype=np.uint8)  # Initialize mask to black

        regions = value["regions"]
        for region in regions:
            shape_attributes = region["shape_attributes"]
            shape_type = shape_attributes["name"]
            if shape_type == "polygon":
                x_points = shape_attributes["all_points_x"]
                y_points = shape_attributes["all_points_y"]
            else:
                print("we are working with polygon annotations!")
            region_attributes = region["region_attributes"]
            class_type = region_attributes["name"].strip()

            # Set the color based on the class_type, or use a default color if the class is not in the classes dictionary
            color = classes.get(class_type, (255, 255, 255)) # Default color is white

            contours = []

            for x, y in zip(x_points, y_points):
                contours.append((x, y))
            contours = np.array(contours)

            cv2.drawContours(mask, [contours], -1, color, -1)

            # If class_type not already in used_classes, add it
            if class_type not in used_classes:
                used_classes[class_type] = color

        cv2.imwrite(f"{msk_dir}/{filename}", mask)

        # Create the overlay
        overlay = cv2.addWeighted(img, 0.5, mask, 0.5, 0)

        # Draw the legend on the overlay
        legend_start_x = w - 200 # start 200 pixels from the right
        legend_start_y = 20 # start 20 pixels from the top
        legend_gap = 30 # 30 pixels gap between each legend item
        for i, (class_type, color) in enumerate(used_classes.items()):
            legend_y = legend_start_y + i * legend_gap
            cv2.rectangle(overlay, (legend_start_x, legend_y), (legend_start_x + 20, legend_y + 20), color, -1) # draw a color square
            cv2.putText(overlay, class_type, (legend_start_x + 30, legend_y + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1) # draw the class name

        cv2.imwrite(f"{overlay_dir}/{filename}", overlay)


def process_json_files(json_folder, img_dir, msk_dir, overlay_dir):
    """
    Loops through all JSON files in provided directory, and uses them to create masks and overlays for corresponding images.

    Args:
        json_folder (str): Directory containing the JSON files.
        img_dir (str): Directory containing the original images.
        msk_dir (str): Directory to save the mask images.
        overlay_dir (str): Directory to save the overlay images.
    """

    if not os.path.exists(msk_dir):
        os.makedirs(msk_dir)

    if not os.path.exists(overlay_dir):
        os.makedirs(overlay_dir)

    # Loop through all files in the json folder
    for filename in os.listdir(json_folder):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            filepath = os.path.join(json_folder, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                create_masks_overlays(data, img_dir, msk_dir, overlay_dir)

json_folder = ''  # Provide path
img_dir = ''  # Provide path
msk_dir = ''  # Provide path
overlay_dir = ''  # Provide path

process_json_files(json_folder, img_dir, msk_dir, overlay_dir)