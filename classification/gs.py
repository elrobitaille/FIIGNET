import os
import shutil
from PIL import Image

# Define the source and target directories
source_dir = '/home/ugrad/serius/edgarrobitaille/FIIGNET/classification/ichtesting'
target_dir = '/home/ugrad/serius/edgarrobitaille/FIIGNET/classification/gsichtesting'

# Copy the directory
shutil.copytree(source_dir, target_dir)

# Walk through target directory and convert all images to grayscale
for foldername, subfolders, filenames in os.walk(target_dir):
    for filename in filenames:
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(foldername, filename)
            img = Image.open(img_path).convert('L')
            img.save(img_path)

print("Finished processing.")
