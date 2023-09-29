import os
import plistlib
from PIL import Image

def cut_images(plist_path, image_dir):
    # Load the PLIST file
    with open(plist_path, 'rb') as fp:
        plist = plistlib.load(fp)

    # Load the original image
    original_image_path = os.path.join(image_dir, plist['metadata']['realTextureFileName'])
    
    # Check if the original image exists
    if not os.path.exists(original_image_path):
        print(f"Skipping {plist_path}. The original image does not exist.")
        return
    
    original_image = Image.open(original_image_path)

    # Loop through the frames and cut the images
    frames = plist['frames']
    extracted_count = 0
    for frame_name, frame_data in frames.items():
        # Get the sprite size and offset
        sprite_size = tuple(int(x) for x in frame_data['spriteSize'].strip('{}').split(','))
        sprite_offset = tuple(int(x) for x in frame_data['spriteOffset'].strip('{}').split(','))

        # Get the texture rectangle
        texture_rect_str = frame_data['textureRect'].strip('{}')
        texture_rect_parts = texture_rect_str.split(',')
        texture_rect = tuple(int(part.strip('{}')) for part in texture_rect_parts)

        # Determine if the image needs to be rotated
        needs_rotation = frame_data.get('textureRotated', False)

        # Determine the cropping coordinates
        if needs_rotation:
            x, y, h, w = texture_rect[0], texture_rect[1], texture_rect[2], texture_rect[3]
            texture_rect = (y, x, w, h)
        else:
            x, y, w, h = texture_rect[0], texture_rect[1], texture_rect[2], texture_rect[3]

        # Create the cropped image
        cropped_image = original_image.crop((x, y, x + w, y + h))

        # Rotate the image if needed
        if needs_rotation:
            cropped_image = cropped_image.transpose(method=Image.ROTATE_90)

        # Create the output directory if it doesn't exist
        output_dir = os.path.join(image_dir, os.path.dirname(frame_name))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save the cropped image
        output_path = os.path.join(image_dir, frame_name)
        cropped_image.save(output_path)
        extracted_count += 1
        print(f"Extraction {frame_name} Successful")

    return extracted_count

def process_dir(directory):
    # Get a list of all PLIST files in the directory
    plist_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.plist')]

    # Process each PLIST file
    total_count = 0
    success_count = 0
    for plist_file in plist_files:
        image_dir = os.path.dirname(plist_file)
        extracted_count = cut_images(plist_file, image_dir)
        if extracted_count is not None:
            success_count += 1
            total_count += extracted_count

    print(f"\nAll extraction is done. \nTotal {len(plist_files)} plist file has been checked. \n{success_count} plist file successfully extracted {total_count} images.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path', help='Path to the directory containing the image and PLIST files, or a path to a single PLIST file')
    args = parser.parse_args()

    if os.path.isdir(args.input_path):
        process_dir(args.input_path)
    else:
        plist_file = args.input_path
        image_dir = os.path.dirname(plist_file)
        cut_images(plist_file, image_dir)
        
        
        
# Attention !
# This script will only valid for the image package. 
# The image must be in PNG. 
# Don't forget to change the file name to the matching plist file. 

# How to use : Image Package Unpacker Script

# 1. open cmd / command prompt
# 2. write the location of the script (example below)
# cd C:\Identity V Files\Assets
# 3. write python convert.py (location of png images and plist files)
# python unpack.py "C:\Identity V Files\Assets\Archive"
# 4. done, you have successfully unpack the image into several pieces

# the script will create a folder according to the plist content.
# the script also automatically overwrite the unpack result.
# if the image is the same, the script won't overwrite it
