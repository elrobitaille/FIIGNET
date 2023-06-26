import os
import argparse
from PIL import Image, ImageEnhance

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def rotate_image(image, degrees):
    return image.rotate(degrees)

def flip_image(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def main(input_directory, output_directory, brightness_values, rotation_values):
    # Loop over all files in the directory
    try: 
        for filename in os.listdir(input_directory):
            if filename.endswith('.jpg') or filename.endswith('.png'): 
                # Open image file
                img = Image.open(os.path.join(input_directory, filename))
                
                for brightness in brightness_values:
                    for rotation in rotation_values:
                        # Print out filename and augmentation parameters
                        print(f"Augmenting: {filename} with brightness={brightness} and rotation={rotation}")
                        # Adjust brightness
                        img_augmented = adjust_brightness(img, brightness)
                        # Rotate image
                        img_augmented = rotate_image(img_augmented, rotation)
                        # Save the image back to the output directory
                        img_augmented.save(os.path.join(output_directory, f"augmented_b_{brightness}_r_{rotation}_" + filename))
                        
                # Flip image and save
                print(f"Flipping: {filename}")
                img_flipped = flip_image(img)
                img_flipped.save(os.path.join(output_directory, "flipped_" + filename))
                
    except Exception as e:
        print(f"Failed to augment images: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Apply data augmentation to images.')
    parser.add_argument('-i', '--input_path', required=True, help='Input directory of images')
    parser.add_argument('-o', '--output_path', required=True, help='Output directory for augmented images')
    args = parser.parse_args()

    # Change to add more values if you want more augments 
    brightness_values = [0.8, 1.2]
    rotation_values = [0, 90]
    
    main(args.input_path, args.output_path, brightness_values, rotation_values)
