import cv2
import os
import argparse
import numpy as np

def sharpen_image(img, sigma=0.25, strength=0.25):
    blurred = cv2.GaussianBlur(img, (0, 0), sigma)
    sharpened = cv2.addWeighted(img, 1.0 + strength, blurred, -strength, 0)
    return sharpened

def apply_clahe(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])
    img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    return img_output

def process_image(image_path, output_dir, filters):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Failed to load image at path: {image_path}")
            return
        for name, function in filters.items():
            if function is not None:
                img = function(img)
        os.makedirs(output_dir, exist_ok=True)
        filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, filename)
        print(f"Saving image to path: {output_path}")
        cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # Save in PNG format with no compression
    except Exception as e:
        print(f"An error occurred while processing image at path: {image_path}. Error: {str(e)}")

def process_directory(input_path, output_path, filters):
    for filename in os.listdir(input_path):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            file_path = os.path.join(input_path, filename)
            process_image(file_path, output_path, filters)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process images with various filters.')
    parser.add_argument('input_path', help='Directory of input images.')
    parser.add_argument('output_path', help='Directory to save processed images.')
    parser.add_argument('--sharpen', action='store_true', help='Apply Unsharp Mask sharpening.')
    parser.add_argument('--clahe', action='store_true', help='Apply CLAHE.')
    args = parser.parse_args()
    filters = {
        'sharpen': sharpen_image if args.sharpen else None,
        'clahe': apply_clahe if args.clahe else None,
    }
    process_directory(args.input_path, args.output_path, filters)
