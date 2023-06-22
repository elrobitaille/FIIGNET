import os
import argparse
from PIL import Image, ImageEnhance

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def rotate_image(image, degrees):
    return image.rotate(degrees)

def main(directory, brightness, rotation):
    # Loop over all files in the directory
    try: 
        for filename in os.listdir(directory):
            if filename.endswith('.jpg') or filename.endswith('.png'): 
                # Open image file
                img = Image.open(os.path.join(directory, filename))
                # Adjust brightness
                img = adjust_brightness(img, brightness)
                # Rotate image
                img = rotate_image(img, rotation)
                # Save the image back to the same file
                img.save(os.path.join(directory, "augmented_" + filename))
    except:
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply data augmentation to images.')
    parser.add_argument('-d', '--dir', required=True, help='Directory of images')
    parser.add_argument('-b', '--brightness', type=float, default=1.0, help='Brightness adjustment factor')
    parser.add_argument('-r', '--rotation', type=float, default=0.0, help='Rotation angle in degrees')
    args = parser.parse_args()

    main(args.dir, args.brightness, args.rotation)
