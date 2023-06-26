import sys
import os
from PIL import Image, ImageOps

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(filename)[1].lower()
    return ext in image_extensions

def resize_image(image_path, output_path, output_size=(1920, 1080), padding=False):
    try: 
        with Image.open(image_path) as img:
            if padding:
                longest_side = max(img.size)
                horizontal_padding = (longest_side - img.size[0]) / 2
                vertical_padding = (longest_side - img.size[1]) / 2
                img = img.crop(
                    (
                        -horizontal_padding,
                        -vertical_padding,
                        img.size[0] + horizontal_padding,
                        img.size[1] + vertical_padding
                    )
                )
                img = ImageOps.expand(img, border=int(min(horizontal_padding, vertical_padding)), fill='black')

            img_resized = img.resize(output_size)

            # Prepare the output path
            filename = os.path.basename(image_path)
            image_output_path = os.path.join(output_path, filename)

            # Print out the current operation
            print(f"Resizing image: {image_path}")
            print(f"Saving resized image to path: {image_output_path}")

            # Save the resized image
            img_resized.save(image_output_path)
    except Exception as e:
         print(f"An error occurred while processing image at path: {image_path}. Error: {str(e)}")

def resize_directory(directory_path, output_path, output_size=(1920, 1080), padding=False):
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    # Iterate through each file in the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                resize_image(file_path, output_path, output_size, padding)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Resize images to a specific size.')
    parser.add_argument('input_path', help='Directory of input images.')
    parser.add_argument('output_path', help='Directory to save processed images.')
    parser.add_argument('--width', type=int, default=1920, help='Width to resize images to.')
    parser.add_argument('--height', type=int, default=1080, help='Height to resize images to.')
    parser.add_argument('--padding', action='store_true', help='Whether to add padding when resizing.')

    args = parser.parse_args()

    output_size = (args.width, args.height)
    print(f"Resizing images to: {output_size}")

    resize_directory(args.input_path, args.output_path, output_size, args.padding)
