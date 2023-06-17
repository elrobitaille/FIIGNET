import sys
import os
from PIL import Image

def is_image_file(filename):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(filename)[1].lower()
    return ext in image_extensions

def resize_image(image_path, output_dir, output_size=(1920, 1080)):
    with Image.open(image_path) as img:
        img_resized = img.resize(output_size)

        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Prepare the output path
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)

        # Save the resized image
        img_resized.save(output_path)

def resize_directory(directory_path, output_dir):
    # Iterate through each file in the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if is_image_file(file_path):
                resize_image(file_path, output_dir)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python resize.py [directory_path] [output_dir]")
        sys.exit(1)

    directory_path = sys.argv[1]
    output_dir = sys.argv[2]

    # Resize images in the specified directory recursively
    resize_directory(directory_path, output_dir)

