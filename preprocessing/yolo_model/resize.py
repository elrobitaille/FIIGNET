import sys
import os
from PIL import Image

#python resize.py "directory"

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(filename)[1].lower()
    return ext in image_extensions

def resize_image(image_path, output_size=(1920, 1080)):
    with Image.open(image_path) as img:
        img_resized = img.resize(output_size)

        # Create output directory if it doesn't exist
        output_dir = 'resized_img'
        os.makedirs(output_dir, exist_ok=True)

        # Prepare the output path
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)

        # Save the resized image
        img_resized.save(output_path)

def resize_directory(directory_path):
    # Iterate through each file in the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                resize_image(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python resize.py [directory_path]")
        sys.exit(1)

    directory_path = sys.argv[1]

    # Resize images in the specified directory recursively
    resize_directory(directory_path)
